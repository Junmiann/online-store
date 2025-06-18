from flask import Flask, render_template, flash, redirect, url_for, request, Blueprint
from db import *
from utils import *

app = Flask(__name__)

product_bp = Blueprint('product', __name__, url_prefix='')

@product_bp.route("/product/<int:product_id>")
def product(product_id):
    cur = con.cursor()
    cur.callproc("get_product_by_id", [product_id])
    selected_product = cur.fetchall()
    return render_template("/product.html", product_id=product_id, selected_product=selected_product)

@product_bp.route("/search")
def search():
    query = request.args.get('query', '')

    cur = con.cursor()
    cur.callproc("search_products", [query])
    search_results = cur.fetchall()
    cur.close()

    if search_results:
        product_id = search_results[0][0]
        return redirect(url_for("product.product", product_id=product_id))
    else:
        flash("No products found matching the query")
        return redirect(url_for("index"))