from flask import Flask, render_template, flash, redirect, url_for, session, Blueprint
from db import *
from utils import *
from models.userOrder import UserOrder
from models.cart import Cart

app = Flask(__name__)

orders_bp = Blueprint('orders', __name__, url_prefix='')

@orders_bp.route("/orders/order_details/<int:order_id>")
def user_order_details(order_id):
    user = session.get("user")
    user_orders_details = UserOrder.get_user_order_details(con, order_id)
    user_order_products = UserOrder.get_user_order_products(con, order_id)
    return render_template("/orders/order_details.html", user=user, order_id=order_id, user_orders=user_orders_details, user_order_products=user_order_products)

@orders_bp.route("/order_check_out/<int:order_id>", methods=["POST"])
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