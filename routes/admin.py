from flask import Flask, render_template, session, request, Blueprint, redirect, url_for
from db import *

app = Flask(__name__)

admin_dashboard_bp = Blueprint('admin_dashboard', __name__, url_prefix='')

@admin_dashboard_bp.route("/admin/<section>")
def admin_dashboard(section):
    user = session.get("user")
    cur = con.cursor()

    suppliers = []

    if section == "orders":
        cur.callproc("all_orders")
        headers = ["Order ID", "Date", "Total", "Customer ID", "Status"]
        data = cur.fetchall()

    elif section == "products":
        cur.callproc("all_products")
        headers = ["Product ID", "Name", "Description","Image", "Quantity", "Price", "Supplier ID"]
        data = cur.fetchall()

        cur.execute("SELECT supplier_id, name FROM supplier")
        suppliers = cur.fetchall()

    cur.close()

    return render_template("/admin_dashboard.html", user=user, section=section, table_headers=headers, table_data=data, suppliers=suppliers)

@admin_dashboard_bp.route("/update_order_status/<int:order_id>", methods=["POST"])
def update_order_status(order_id):
    cur = con.cursor()
    updated_order_status = request.form["status"]
    cur.callproc("update_order_status", [order_id, updated_order_status.capitalize(),])
    con.commit()
    cur.close()
    return redirect(url_for("admin_dashboard.admin_dashboard", section="orders"))

# Add new product
@admin_dashboard_bp.route("/add_new_product", methods=["POST"])
def add_new_product():
    cur = con.cursor()

    name = request.form["name"]
    description = request.form["description"]
    img_url = request.form["image_url"]
    quantity = request.form["quantity"]
    price = request.form["price"]
    supplier_id = request.form["supplier_id"]

    cur.callproc("add_new_product", [name, description, img_url, quantity, price, supplier_id,])
    con.commit()
    cur.close()
    return redirect(url_for("admin_dashboard.admin_dashboard", section="products"))

# Edit product information
@admin_dashboard_bp.route("/edit_product", methods=["POST"])
def edit_product():
    cur = con.cursor()
    
    product_id = request.form["product_id"]
    name = request.form["name"]
    description = request.form["description"]
    img_url = request.form["image_url"]
    quantity = request.form["quantity"]
    price = request.form["price"]
    supplier_id = request.form["supplier_id"]

    cur.callproc("edit_product", [product_id, name, description, img_url, quantity, price, supplier_id,])
    con.commit()
    cur.close()
    return redirect(url_for("admin_dashboard.admin_dashboard", section="products"))