from flask import Flask, render_template, session, Blueprint
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
        headers = ["Product ID", "Name", "Image", "Quantity", "Price", "Supplier ID"]

    rows = cur.fetchall()
    cur.close()

    return render_template("/admin/dashboard.html", user=user, section=section, table_headers=headers, table_data=rows)
