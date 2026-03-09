from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.database import Product, Order, PriceHistory, db
from datetime import datetime, date
import sqlalchemy as sa
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin/dashboard')
@admin_required
def dashboard():
    products = Product.query.all()
    
    # Calculate price change %
    for p in products:
        p.change_pct = round(((p.current_price - p.base_price) / p.base_price) * 100, 2)
        
    # Total orders today
    today = date.today()
    orders_today = Order.query.filter(sa.func.date(Order.created_at) == today).count()
    
    # Top 5 most dynamic products (highest volatility in last 10 entries)
    # This is a simplified metric for the dashboard
    dynamic_products = []
    for p in products:
        recent_prices = PriceHistory.query.filter_by(product_id=p.id).order_by(PriceHistory.timestamp.desc()).limit(5).all()
        if len(recent_prices) > 1:
            prices = [h.price for h in recent_prices]
            volatility = max(prices) - min(prices)
            dynamic_products.append({'name': p.name, 'volatility': volatility})
            
    dynamic_products = sorted(dynamic_products, key=lambda x: x['volatility'], reverse=True)[:5]
    
    return render_template('admin_dashboard.html', 
                           products=products, 
                           orders_today=orders_today,
                           dynamic_products=dynamic_products)

@admin_bp.route('/admin/product/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        base_price = float(request.form.get('base_price'))
        category = request.form.get('category')
        stock = int(request.form.get('stock'))
        image_url = request.form.get('image_url')

        new_product = Product(
            name=name,
            description=description,
            base_price=base_price,
            current_price=base_price,
            category=category,
            stock=stock,
            image_url=image_url
        )
        db.session.add(new_product)
        db.session.commit()
        
        # Add initial price history
        hist = PriceHistory(product_id=new_product.id, price=base_price, demand_score=0.0)
        db.session.add(hist)
        db.session.commit()

        flash('Product added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin_product_form.html', title='Add Product')

@admin_bp.route('/admin/product/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.base_price = float(request.form.get('base_price'))
        product.category = request.form.get('category')
        product.stock = int(request.form.get('stock'))
        product.image_url = request.form.get('image_url')

        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin_product_form.html', title='Edit Product', product=product)

@admin_bp.route('/admin/product/delete/<int:id>', methods=['POST'])
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))
