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
    is_admin = user[9] == True
    user_orders_details = UserOrder.get_user_order_details(con, order_id)
    user_order_products = UserOrder.get_user_order_products(con, order_id)
    return render_template("/order_details.html", user=user, order_id=order_id, user_orders=user_orders_details, user_order_products=user_order_products, is_admin=is_admin)

# TODO: The function is too long, shorten it for readability and maintainability
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
    
    user_cart_items = Cart.get_cart_products(con, order_id)

    with con.cursor() as cur:
        for item in user_cart_items:
            product_id = item[4]
            user_chosen_quantity = item[2]
            
            cur.callproc("get_product_by_id", [product_id])
            product = cur.fetchone()
            product_name = product[1]
            left_in_stock = product[6]
            
            if left_in_stock == 0:
                con.rollback()
                flash(f"{product_name} is unfortunately out of stock!")
                return redirect(url_for("cart.cart"))
            elif user_chosen_quantity > left_in_stock:
                con.rollback()
                flash(f"The quantity you selected for {product_name} exceeds our current stock.")
                return redirect(url_for("cart.cart"))
    
        for item in user_cart_items:
            product_id = item[4]
            user_chosen_quantity = item[2]
            cur.callproc("update_product_quantity", [product_id, user_chosen_quantity])

    con.commit()
    Cart.check_out(con, user[0], order_id)
    return render_template("/cart.html", checkout_success=True, user=session.get("user"))