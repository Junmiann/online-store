from flask import Flask, flash, redirect, url_for, request, Blueprint
from db import *
from utils import *

app = Flask(__name__)

search_bp = Blueprint('search', __name__, url_prefix='')

@search_bp.route("/search")
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