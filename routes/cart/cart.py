from flask import Flask, render_template, flash, redirect, url_for, session, Blueprint
from db import *
from utils import *
from models.userOrder import UserOrder
from models.cart import Cart

app = Flask(__name__)

cart_bp = Blueprint('cart', __name__, url_prefix='')

@cart_bp.route("/cart")
def cart():
    user = session.get("user")

    if user:
        # Check if user has an on-going order
        order_id = check_order_status()

        if order_id:
            # Get all products (to display the added products into the cart)
            list_products = all_products()

            # Get order details and products from DB
            user_orders_details = UserOrder.get_user_order_details(con, order_id)
            user_order_products = UserOrder.get_user_order_products(con, order_id)

            # Render shopping cart page with all data
            return render_template("/cart/cart.html", user=user, order_id=order_id, list_products=list_products, user_orders_details=user_orders_details, user_order_products=user_order_products)
        else:
            return render_template("/cart/cart.html", user=user)
    else:
        flash("Log in to check your shopping cart!")
        return redirect(url_for("login.login"))

@cart_bp.route("/remove_item_from_cart/<int:product_id>", methods=["POST"])
def remove_item_from_cart(product_id):
    """
    Remove a product from the user's shopping cart by product_id
    """
    order_id = check_order_status()

    Cart.get_product(con, product_id)
    Cart.delete_product(con, order_id, product_id)
    
    return redirect(url_for("cart.cart"))

@cart_bp.route("/cart/order_check_out/<int:order_id>", methods=["POST"])
def order_check_out(order_id):
    """
    Process check out for the order with the given order_id
    """
    user = session.get("user")
    order_id = check_order_status()

    user_orders_details = UserOrder.get_user_order_details(con, order_id)
    order_sum = user_orders_details[0][2]

    if order_sum == 0:
        flash("Please add an item into the cart before checking out!")
        return redirect(url_for("cart.cart"))
    
    else: 
        Cart.check_out(con, user[0], order_id)
        return render_template("/cart/cart.html", checkout_success=True, user=session.get("user"))