import uuid
from models import Cart, Product
from app import db


class CartService:
    def add_to_cart(self, user_id: str, product_id: str, quantity: int = 1):
        cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += quantity
            cart_item.updated_at = db.func.now()
        else:
            cart_item = Cart(
                id=str(uuid.uuid4()),
                user_id=user_id,
                product_id=product_id,
                quantity=quantity,
            )
            db.session.add(cart_item)
        db.session.commit()
        return cart_item

    def get_cart(self, user_id: str):
        cart_items = Cart.query.filter_by(user_id=user_id).all()

        return [
            {
                **item.to_dict(),
                "product": Product.query.get(item.product_id).to_dict()
                if Product.query.get(item.product_id)
                else None,
            }
            for item in cart_items
        ]
