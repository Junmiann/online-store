from flask import Flask, render_template, flash, redirect, url_for, request, session, Blueprint
from db import *
from utils import *

app = Flask(__name__)

product_bp = Blueprint('product', __name__, url_prefix='')

@product_bp.route("/product/<int:product_id>")
def product(product_id):
    cur = con.cursor()
    cur.callproc("get_product_by_id", [product_id])
    selected_product = cur.fetchall()
    return render_template("product.html", product_id=product_id, selected_product=selected_product)

@product_bp.route("/add_to_cart/<int:product_id>", methods=["POST"])
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
        available_quantity = cur.fetchone()[5]

        if product_quantity > available_quantity:
            flash("Can't add product(s): Requested quantity exceeds available quantity")
            return redirect(url_for("product", product_id=product_id))

        cur.callproc("check_product_in_cart", [order_id, product_id])
        existing_product = cur.fetchall()
        if existing_product:
            cur.callproc("update_product_quantity", [product_quantity, order_id, product_id])
        else:
            cur.callproc("add_product", [order_id, user[0], product_id, product_quantity])

        cur.callproc("update_order_total_price", [order_id])
        con.commit()
        cur.close()

        return redirect(url_for("index"))