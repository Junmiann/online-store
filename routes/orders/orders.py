from flask import Flask, render_template, session, Blueprint
from db import *
from models.userOrder import UserOrder

app = Flask(__name__)

orders_bp = Blueprint('orders', __name__, url_prefix='')

@orders_bp.route("/orders/order_details/<int:order_id>")
def user_order_details(order_id):
    user = session.get("user")
    user_orders_details = UserOrder.get_user_order_details(con, order_id)
    user_order_products = UserOrder.get_user_order_products(con, order_id)
    return render_template("/orders/order_details.html", user=user, order_id=order_id, user_orders=user_orders_details, user_order_products=user_order_products)