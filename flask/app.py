# app.py
from sqlalchemy import event
from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from datetime import datetime

Config.create_database()

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Models
class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    sku = db.Column(db.String, unique=True, nullable=False)
    category = db.Column(db.String)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    stock_levels = db.relationship('StockLevel', back_populates='product', cascade='all, delete', lazy=True)

class StockLevel(db.Model):
    __tablename__ = 'stock_levels'
    stock_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    threshold = db.Column(db.Integer, default=10)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    product = db.relationship('Product', back_populates='stock_levels', lazy=True)

class RestockingLog(db.Model):
    __tablename__ = 'restocking_logs'
    restock_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id', ondelete='CASCADE'), nullable=False)
    quantity_added = db.Column(db.Integer, nullable=False)
    restock_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.String)

# Log after insert
@event.listens_for(StockLevel, 'after_insert')
def log_stock_insert(mapper, connection, target):
    connection.execute(
        RestockingLog.__table__.insert(),
        {
            'product_id': target.product_id,
            'quantity_added': target.quantity,
            'restock_date': datetime.utcnow(),
            'notes': 'Initial stock insert'
        }
    )

# Log after update
@event.listens_for(StockLevel, 'after_update')
def log_stock_update(mapper, connection, target):
    connection.execute(
        RestockingLog.__table__.insert(),
        {
            'product_id': target.product_id,
            'quantity_added': target.quantity,  # Log full new quantity
            'restock_date': datetime.utcnow(),
            'notes': 'Stock level updated'
        }
    )

def configure_stock(product_id, quantity):
    """
    Updates the stock level of a product.

    Args:
        product_id: The product to update.
        quantity: The amount to update.

    Returns:
        None.
    """

    # Get the stock row of the required product
    stock = StockLevel.query.filter_by(product_id=product_id).first()
    
    # Create if it doesn't exist. Otherwise, add it to the current sum.
    if not stock:
        stock = StockLevel(product_id=product_id, quantity=quantity)
        db.session.add(stock)

    else:
        stock.quantity += quantity
        stock.updated_at = datetime.utcnow()

# Add new product
@app.route('/api/products', methods=['POST'])
def add_product():

    data = request.json

    # Extract stock values if provided
    quantity = data.pop('quantity', 0)  # default to 0 if not provided
    threshold = data.pop('threshold', 10)  # default threshold

    try:
        # Create the product
        product = Product(**data)
        db.session.add(product)
        db.session.flush()  # get product_id before commit

        # Create the stock level entry
        stock = StockLevel(
            product_id=product.product_id,
            quantity=quantity,
            threshold=threshold
        )
        db.session.add(stock)
        db.session.commit()

        return jsonify({
            'message': 'Product and stock level added',
            'product_id': product.product_id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Get details of specific product
@app.route('/api/products', methods=['GET'])
def get_products():

    rows = db.session.query(Product).join(StockLevel.product).all()
    products = []

    for product in rows:

        products.append({
            'id': product.product_id,
            'name': product.name,
            'description': product.description,
            'sku': product.sku,
            'price': str(product.price),

            # stock levels comes inside a list instead of just the object, so we take index 0
            'quantity': product.stock_levels[0].quantity
        })

    return jsonify(products)

# Get details of specific product
@app.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    product = db.session.query(Product).join(StockLevel.product).filter_by(product_id=id).first()

    return jsonify({
        'id': product.product_id,
        'name': product.name,
        'sku': product.sku,
        'price': str(product.price),
        'quantity': product.stock_levels[0].quantity
    })

# Update product stock
@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json

    quantity = data.pop('quantity_to_add', None)

    product = Product.query.get_or_404(id)
    for key, value in data.items():
        setattr(product, key, value)

    # If quantity was added, update it accordingly in the table.
    if quantity:
        configure_stock(id, quantity)

    db.session.commit()
    return jsonify({'message': 'Product updated'})

# Delete product
@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'})

# Restock a specific product
@app.route('/api/products/<product_id>/restock', methods=['POST'])
def restock():
    data = request.json

    configure_stock(request.args['product_id'], data['quantity_added'])

    db.session.commit()
    return jsonify({'message': 'Stock updated'}), 201

@app.route('/stock/<int:product_id>', methods=['GET'])
def get_stock(product_id):

    # Fetch stock row of product id
    stock = StockLevel.query.filter_by(product_id=product_id).first_or_404()
    
    return jsonify({
        'product_id': stock.product_id,
        'quantity': stock.quantity,
        'last_updated': stock.updated_at.isoformat()
    })

@app.route('/api/restocks')
def get_restock_history():

    restocks = RestockingLog.query.all()

    results = []

    for restock in restocks:
        results.append({
            'restock_id': restock.restock_id,
            'product_id': restock.product_id,
            'quantity_added': restock.quantity_added,
            'restock_date': restock.restock_date,
            'notes': restock.notes
        })

    return results


@app.route('/api/products/low-stock', methods=['GET'])
def get_low_stock_products():

    # Fetch rows of stock items of low threshold
    low_stock_items = StockLevel.query.filter(StockLevel.quantity <= StockLevel.threshold).all()

    result = []

    # Iterate over each row, jsonify and store in array
    for item in low_stock_items:
        product = Product.query.get(item.product_id)
        result.append({
            'product_id': item.product_id,
            'product_name': product.name if product else 'Unknown',
            'quantity': item.quantity,
            'threshold': item.threshold
        })

    return jsonify(result)


# Initialize
if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True, port=80, host="0.0.0.0")

# Problems:
# Queries updating stock_level
# Must update through stock logs as it automatically updates stock_level with trigger
# Check put function as it can also update stock levels (only RESTOCKS happen through stock logs) 
# what is Fetch stock trend data for dashboard visualization 

# TO DO:
# Fix put function - WE DID LOL
# Create DB through script
# Add log trigger - WE DID LOL