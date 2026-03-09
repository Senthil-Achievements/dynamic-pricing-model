from flask import Blueprint, jsonify, request
from models.database import Product, PriceHistory
from utils.pricing_engine import PricingEngine

api_bp = Blueprint('api', __name__)
engine = PricingEngine()

@api_bp.route('/api/price/<int:product_id>')
def get_price(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'current_price': product.current_price,
        'last_updated': product.last_updated.isoformat()
    })

@api_bp.route('/api/update-prices', methods=['POST'])
def update_prices():
    # This is called by the scheduler or manually
    engine.update_all_prices()
    return jsonify({'status': 'success', 'message': 'All prices recalculated'})
