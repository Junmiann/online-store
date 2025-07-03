from flask import Flask, render_template, session, request, Blueprint, redirect, url_for
from db import *

app = Flask(__name__)

admin_dashboard_bp = Blueprint('admin_dashboard', __name__, url_prefix='')

@admin_dashboard_bp.route("/admin/<section>")
def admin_dashboard(section):
    user = session.get("user")
    cur = con.cursor()

    if section == "orders":
        cur.callproc("all_orders")
        headers = ["Order ID", "Date", "Total", "Customer ID", "Status"]
    elif section == "products":
        cur.callproc("all_products")
        headers = ["Product ID", "Name", "Description","Image", "Quantity", "Price", "Supplier ID"]

    rows = cur.fetchall()
    cur.close()

    return render_template("/admin_dashboard.html", user=user, section=section, table_headers=headers, table_data=rows)

@admin_dashboard_bp.route("/update_order_status/<int:order_id>", methods=["POST"])
def update_order_status(order_id):
    cur = con.cursor()

    updated_order_status = request.form["status"]
    cur.callproc("update_order_status", [order_id, updated_order_status.capitalize(),])
    print(updated_order_status)
    con.commit()
    cur.close()
    return redirect(url_for("admin_dashboard.admin_dashboard", section="orders"))
