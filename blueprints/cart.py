from flask import Flask, render_template, flash, redirect, url_for, session, Blueprint
from db import *
from utils import *

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
            list_products = sp_all_products()

            # Get order details and products from DB
            cur = con.cursor()
            cur.callproc("get_order_details", [order_id])
            user_order = cur.fetchall()

            cur.callproc("get_order_products", [order_id])
            user_order_products = cur.fetchall()

            # Render shopping cart page with all data
            return render_template("/cart.html", user=user, order_id=order_id, list_products=list_products, user_order=user_order, user_order_products=user_order_products)
        else:
            render_template("/cart.html", user=user)
    else:
        flash("Log in to check your shopping cart!")
        return redirect(url_for("login.login"))

@cart_bp.route("/remove_item_from_cart/<int:product_id>", methods=["POST"])
def remove_item_from_cart(product_id):
    """
    Remove a product from the user's shopping cart by product_id
    """
    order_id = check_order_status()

    cur = con.cursor()

    cur.callproc("get_product_by_id", [product_id])
    cur.fetchall()

    cur.callproc("delete_product", [order_id, product_id])
    con.commit()
    cur.close()
    
    return redirect(url_for("cart.cart"))

@cart_bp.route("/cart/order_check_out/<int:order_id>", methods=["POST"])
def order_check_out(order_id):
    """
    Process check out for the order with the given order_id
    """
    user = session.get("user")

    order_id = check_order_status()

    cur = con.cursor()
    cur.callproc("get_order_details", order_id)
    order_details = cur.fetchall()
    order_sum = order_details[0][2]

    if order_sum == 0:
        flash("Please add an item into the cart before checking out!")
        return redirect(url_for("cart.cart"))
    
    else: 
        cur.callproc("order_check_out", [user[0], order_id])
        con.commit()
        cur.close()
        return render_template("/cart.html", checkout_success=True, user=session.get("user"))