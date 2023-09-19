from flask import Flask, request, jsonify

# Initialize the Flask application
app = Flask(__name__)

# Sample product data
products = [
    {
        "id": 1,
        "name": "Product 1",
        "price": 10.99,
        "quantity": 50,
    },
    {
        "id": 2,
        "name": "Product 2",
        "price": 5.99,
        "quantity": 100,
    },
        {
        "id": 3,
        "name": "Product 3",
        "price": 7.99,
        "quantity": 50,
    }
]

# Route to retrieve a list of available grocery products
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

# Route to get details about a specific product by its unique ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product is not None:
        return jsonify(product)
    else:
        return jsonify({"error": "Product not found"}), 404

# Route to add new grocery products to the inventory
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json(force=True)
    if 'name' in data and 'price' in data and 'quantity' in data:
        new_product = {
            "id": len(products) + 1,
            "name": data['name'],
            "price": data['price'],
            "quantity": data['quantity'],
        }
        products.append(new_product)
        return jsonify({"message": "Product added successfully"}), 201
    else:
        return jsonify({"error": "Invalid product data"}), 400

@app.route('/products/<int:product_id>/update_quantity', methods=['POST'])
def update_product_quantity(product_id):
    data = request.get_json(force=True)
    new_quantity = data.get("quantity")

    product = next((p for p in products if p['id'] == product_id), None)
    if product is not None:
        product['quantity'] = new_quantity
        return jsonify({"message": "Product quantity updated successfully"}), 200
    else:
        return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
