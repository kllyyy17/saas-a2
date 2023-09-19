from flask import Flask, request, jsonify
import requests

# Initialize the Flask application
app = Flask(__name__)

# Sample cart data (in-memory storage for simplicity)
carts = {}

# Product Service URL (Update with the actual URL)
PRODUCT_SERVICE_URL = "http://127.0.0.1:5000"

# Route to retrieve the current contents of a user's shopping cart
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    if user_id in carts:
        return jsonify(carts[user_id])
    else:
        return jsonify({"error": "Cart not found"}), 404

# Route to add a specified quantity of a product to the user's cart
@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    quantity = request.json.get("quantity", 1)  # Default to 1 if quantity not provided
    product = get_product_from_product_service(product_id)
    
    if product:

        if product['quantity'] < quantity:
            return jsonify({"error": "Product quantity in product service is not enough"}), 404

        if user_id not in carts:
            carts[user_id] = {}
        if product_id in carts[user_id]:
            carts[user_id][product_id]['quantity'] += quantity
        else:
            carts[user_id][product_id] = {
                'name': product['name'],
                'quantity': quantity,
                'price': product['price'],
            }

        # Make a request to update the product quantity in product_service
        update_product_quantity(product_id, product['quantity'] - quantity)

        return jsonify({"message": "Product added to cart successfully"}), 201
    else:
        return jsonify({"error": "Product not found"}), 404

# Route to remove a specified quantity of a product from the user's cart
@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    quantity = request.json.get("quantity", 1)  # Default to 1 if quantity not provided
    product = get_product_from_product_service(product_id)

    if user_id in carts and product_id in carts[user_id]:
        if carts[user_id][product_id]['quantity'] >= quantity:
            carts[user_id][product_id]['quantity'] -= quantity
        else:
            return jsonify({"error": "Product quantity in the cart is not enough"}), 404

        if  carts[user_id][product_id]['quantity'] == 0:
            del carts[user_id][product_id]

        # Make a request to update the product quantity in product_service
        update_product_quantity(product_id, product['quantity'] + quantity)
            
        return jsonify({"message": "Product removed from cart successfully"}), 200
    else:
        return jsonify({"error": "Product not found in the cart"}), 404

# Helper function to get product information from the Product Service
def get_product_from_product_service(product_id):
    response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def update_product_quantity(product_id, new_quantity):
    data = {"quantity": new_quantity}
    response = requests.post(
        f"{PRODUCT_SERVICE_URL}/products/{product_id}/update_quantity",
        json=data
    )

    if response.status_code == 200:
        return {"message": "Product quantity updated successfully"}
    elif response.status_code == 404:
        return {"error": "Product not found"}
    else:
        # Log the error for debugging
        print(f"Error: {response.status_code} - {response.text}")
        return {"error": "An unexpected error occurred"}

if __name__ == '__main__':
    app.run(debug=True, port=5001)
