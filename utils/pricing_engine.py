from datetime import datetime
from models.database import db, Product, PriceHistory, Order, OrderItem
from models.pricing_model import PricingModel
import sqlalchemy as sa

class PricingEngine:
    def __init__(self):
        self.ml_model = PricingModel()

    def get_demand_score(self, product_id):
        """
        Calculate demand based on sales velocity in the last 24 hours.
        Weight: 0.5 (as per requirements)
        """
        # Count items sold in the last 24 hours
        yesterday = datetime.utcnow().replace(day=datetime.utcnow().day-1) if datetime.utcnow().day > 1 else datetime.utcnow() # Basic logic
        
        sales_count = db.session.query(sa.func.sum(OrderItem.quantity)).join(Order).filter(
            OrderItem.product_id == product_id,
            Order.created_at >= yesterday
        ).scalar() or 0
        
        # Normalize score between 0 and 10
        score = min(float(sales_count) * 2, 10.0) 
        return score

    def calculate_new_price(self, product):
        """
        Dynamic Pricing Formula:
        optimal_price = ML_prediction
        Rules:
        - Floor: 0.85 * base_price
        - Ceiling: 1.50 * base_price
        - Max change per update: 20%
        """
        now = datetime.now()
        demand_score = self.get_demand_score(product.id)
        
        # Features: hour_of_day, day_of_week, stock_level, demand_score, base_price
        features = [
            now.hour,
            now.weekday(),
            product.stock,
            demand_score,
            product.base_price
        ]
        
        predicted_price = self.ml_model.predict(features)
        
        # Apply Constraints
        floor = product.base_price * 0.85
        ceiling = product.base_price * 1.50
        
        # Apply Floor and Ceiling
        final_price = max(min(predicted_price, ceiling), floor)
        
        # Apply Max Change Per Update (20%)
        max_change = product.current_price * 0.20
        price_diff = final_price - product.current_price
        
        if abs(price_diff) > max_change:
            final_price = product.current_price + (max_change if price_diff > 0 else -max_change)
            
        return round(final_price, 2), demand_score

    def update_all_prices(self):
        products = Product.query.all()
        for product in products:
            new_price, demand_score = self.calculate_new_price(product)
            
            # Save to History
            history = PriceHistory(
                product_id=product.id,
                price=new_price,
                demand_score=demand_score
            )
            db.session.add(history)
            
            # Update current price
            product.current_price = new_price
            product.last_updated = datetime.utcnow()
            
        db.session.commit()
        print(f"Prices updated at {datetime.now()}")
