from flask import Blueprint, request, jsonify
from services.cart_service import CartService

cart_bp = Blueprint("cart", __name__)
cart_service = CartService()


@cart_bp.route("/cart/<user_id>", methods=["GET"])
def get_cart(user_id):
    try:
        cart_items = cart_service.get_cart(user_id)
        return jsonify(cart_items), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@cart_bp.route("/cart/add", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    user_id = data.get("user_id")
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)
    if not user_id or not product_id:
        return jsonify({"error": "user_id and product_id are required"}), 400
    try:
        cart_item = cart_service.add_to_cart(user_id, product_id, quantity)
        return jsonify(
            {
                **cart_item.to_dict(),
                "product": cart_item.product.to_dict()
                if hasattr(cart_item, "product") and cart_item.product
                else None,
            }
        ), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
