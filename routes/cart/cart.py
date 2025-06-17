from flask import Flask, render_template, flash, redirect, url_for, request, session, Blueprint
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
    
@cart_bp.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    user = session.get("user")
    if not user:
        flash("Log in to add products to your shopping cart!")
        return redirect(url_for("login.login"))
    else:
        order_id = check_order_status()

        cur = con.cursor()

        product_quantity = int(request.form["quantity"])
        cur.callproc("get_product_by_id", [product_id])
        
        cur.callproc("check_product_in_cart", [order_id, product_id])
        existing_product = cur.fetchall()
        if existing_product:
            cur.callproc("update_product_quantity", [product_quantity, order_id, product_id])
        else:
            cur.callproc("add_product", [order_id, user[0], product_id, product_quantity])

        cur.callproc("update_order_total_price", [order_id])
        con.commit()
        cur.close()

        flash("The product has been added to cart!")
        return redirect(url_for("product.product", product_id=product_id))

@cart_bp.route("/remove_item_from_cart/<int:product_id>", methods=["POST"])
def remove_item_from_cart(product_id):
    """
    Remove a product from the user's shopping cart by product_id
    """
    order_id = check_order_status()

    Cart.get_product(con, product_id)
    Cart.delete_product(con, order_id, product_id)
    
    return redirect(url_for("cart.cart"))