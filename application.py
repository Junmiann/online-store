from flask import Flask, render_template, flash, redirect, url_for, request, session
from db import *
from blueprints import *
from utils import *

app = Flask(__name__)

order_id = None

app.register_blueprint(product_bp)
app.register_blueprint(login_bp)
app.register_blueprint(user_profile_bp)
app.register_blueprint(cart_bp)

@app.route("/")
def index():
    list_products = sp_all_products()
    user = session.get("user")
    return render_template("index.html", list_products=list_products, user=user)

@app.route("/search")
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

if __name__ == "__main__":
    secret_key = os.getenv("SECRET_KEY")
    app.secret_key = secret_key
    app.run(debug=True)
