from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_required
from models.database import db, Product, Cart, Order, OrderItem, PriceHistory
from datetime import datetime, timedelta
import random

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    featured_products = Product.query.limit(4).all()
    # Also fetch recommendations for the home page
    recommendations = Product.query.order_by(db.func.random()).limit(4).all()
    return render_template('index.html', products=featured_products, recommendations=recommendations)

@main_bp.route('/products')
def all_products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@main_bp.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    # Get last 10 price history entries for the chart
    history = PriceHistory.query.filter_by(product_id=id).order_by(PriceHistory.timestamp.desc()).limit(10).all()
    history.reverse() # Sort chronologically for chart
    
    # Calculate trend
    trend = 'stable'
    if len(history) >= 2:
        if history[-1].price > history[-2].price:
            trend = 'up'
        elif history[-1].price < history[-2].price:
            trend = 'down'
            
    # Recommendations: Fetch 4 products from same category, excluding current
    recommendations = Product.query.filter(Product.category == product.category, Product.id != id).limit(4).all()
    # If not enough in same category, fill with random ones
    if len(recommendations) < 4:
        extra = Product.query.filter(Product.id != id, Product.id.notin_([r.id for r in recommendations])).limit(4 - len(recommendations)).all()
        recommendations.extend(extra)
            
    return render_template('product_detail.html', product=product, history=history, trend=trend, recommendations=recommendations)

@main_bp.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('main.all_products'))
    
    products = Product.query.filter(
        (Product.name.ilike(f'%{query}%')) | 
        (Product.description.ilike(f'%{query}%')) |
        (Product.category.ilike(f'%{query}%'))
    ).all()
    
    return render_template('products.html', products=products, search_query=query)

@main_bp.route('/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    
    item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if item:
        item.quantity += quantity
    else:
        new_item = Cart(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(new_item)
    
    db.session.commit()
    flash('Item added to cart!', 'success')
    return redirect(url_for('main.cart'))

@main_bp.route('/cart')
@login_required
def cart():
    items = Cart.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.current_price * item.quantity for item in items)
    return render_template('cart.html', items=items, total=round(total, 2))

@main_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('main.all_products'))
        
    total_amount = sum(item.product.current_price * item.quantity for item in cart_items)
    
    # Calculate estimated delivery (3-7 days from now)
    delivery_days = random.randint(3, 7)
    est_delivery = datetime.utcnow() + timedelta(days=delivery_days)
    
    new_order = Order(
        user_id=current_user.id, 
        total_amount=total_amount, 
        status='completed',
        estimated_delivery=est_delivery
    )
    db.session.add(new_order)
    db.session.flush() # Get order ID
    
    for item in cart_items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_purchase=item.product.current_price
        )
        # Reduce stock
        item.product.stock -= item.quantity
        db.session.add(order_item)
        db.session.delete(item)
        
    db.session.commit()
    return redirect(url_for('main.order_success', order_id=new_order.id))

@main_bp.route('/order-success/<int:order_id>')
@login_required
def order_success(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        return redirect(url_for('main.index'))
    
    # Calculate days remaining for display
    days_to_go = (order.estimated_delivery - datetime.utcnow()).days + 1
    
    return render_template('order_success.html', order=order, days=max(1, days_to_go))
