from app import app
from models.database import db, Product, User, PriceHistory
from utils.pricing_engine import PricingEngine
import random

def seed():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create Admin
        admin = User(email='admin@example.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)

        # Create User
        user = User(email='user@example.com', role='user')
        user.set_password('user123')
        db.session.add(user)

        categories = ['Electronics', 'Groceries', 'Home & Kitchen']
        
        products_data = [
            ('iPhone 15', 'Latest Apple smartphone', 999.00, categories[0], 50, 'https://images.unsplash.com/photo-1696446701796-da61225697cc?w=800'),
            ('MacBook Air', 'Ultra-thin laptop', 1199.00, categories[0], 30, 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800'),
            ('Sony Headphones', 'Noise cancelling', 349.00, categories[0], 100, 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800'),
            ('Organic Milk', 'Fresh farm milk', 4.50, categories[1], 200, 'https://images.unsplash.com/photo-1563636619-e910f64c1bdf?w=800'),
            ('Avocado 2-Pack', 'Ripe avocados', 3.00, categories[1], 150, 'https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?w=800'),
            ('Coffee Beans', 'Premium Arabica', 18.00, categories[1], 80, 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800'),
            ('Air Fryer', 'Healthy cooking', 120.00, categories[2], 40, 'https://images.unsplash.com/photo-1626074353765-517a681e40be?w=800'),
            ('Cotton Towels', 'Soft and absorbent', 25.00, categories[2], 120, 'https://images.unsplash.com/photo-1583947215259-38e31be8751f?w=800'),
            ('Desk Lamp', 'LED adjustable', 45.00, categories[2], 60, 'https://images.unsplash.com/photo-1534073828943-f801091bb18c?w=800'),
            ('Kitchen Knife Set', 'Professional grade', 85.00, categories[2], 25, 'https://images.unsplash.com/photo-1593611664162-ef74bc56593b?w=800'),
        ]

        products = []
        for name, desc, price, cat, stock, img in products_data:
            p = Product(
                name=name,
                description=desc,
                base_price=price,
                current_price=price,
                category=cat,
                stock=stock,
                image_url=img
            )
            db.session.add(p)
            products.append(p)

        db.session.commit()

        # Seed some price history
        engine = PricingEngine()
        for p in products:
            # Create some fake sales logic for history
            for _ in range(5):
                # Randomly fluctuate price for history
                price = p.base_price * random.uniform(0.9, 1.1)
                hist = PriceHistory(product_id=p.id, price=price, demand_score=random.uniform(1, 8))
                db.session.add(hist)
        
        db.session.commit()
        print("Database seeded with 10 products and initial history.")

if __name__ == '__main__':
    seed()
