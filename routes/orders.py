from flask import Flask, render_template, flash, redirect, url_for, session, Blueprint
from db import *
from utils import *
from models.userOrder import UserOrder
from models.cart import Cart

app = Flask(__name__)

orders_bp = Blueprint('orders', __name__, url_prefix='')

@orders_bp.route("/orders/order_details/<int:order_id>")
def user_order_details(order_id):
    user, _, _, _, is_admin = utils.user_details()
    user_orders_details = UserOrder.get_user_order_details(con, order_id)
    order_info = user_orders_details[0]
    order_date = order_info[1]
    order_total_price = order_info[2]
    order_status = order_info[3]

    user_order_products = UserOrder.get_user_order_products(con, order_id)
    product_info = user_order_products[0]
    product_id = product_info[4]
    product_img = product_info[0]
    product_name = product_info[1]
    product_quantity = product_info[2]
    product_price = product_info[3]

    return render_template("/order_details.html",
                           user=user, 
                           is_admin=is_admin, 
                           order_id=order_id,
                           user_orders=user_orders_details,
                           order_date=order_date, 
                           order_total_price=order_total_price,
                           order_status=order_status,
                           user_order_products=user_order_products,
                           product_id=product_id,
                           product_img=product_img,
                           product_name=product_name,
                           product_quantity=product_quantity,
                           product_price=product_price)

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
        return render_template("/cart.html", checkout_success=True, user=session.get("user"))