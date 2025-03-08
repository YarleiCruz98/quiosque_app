from flask import request, jsonify, Blueprint
from app.models.product_models import Product
from app.config import db

product_blueprint = Blueprint('product_bp', __name__)
@product_blueprint.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        price=data['price'],
        stock=data['stock'],
        description=data.get('description')
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

@product_blueprint.route('/products', methods=['GET'])
def get_product():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products]), 200