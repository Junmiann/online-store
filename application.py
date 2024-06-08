from flask import Flask, render_template, flash, redirect, url_for, request, session
from db import *

app = Flask(__name__)

order_id = None

def sp_all_products():
    cur = con.cursor()
    cur.callproc("sp_all_products")
    list_products = cur.fetchall()
    cur.close()
    return list_products

def check_order_status():
    global order_id
    user = session.get('user')

    cur = con.cursor()
    cur.callproc("check_order_status", [user[0], 'P'])
    order_status = cur.fetchone()

    if order_status:
        order_id = order_status
    else:
        cur.callproc("create_order", [0, user[0]])
        con.commit()
        order_id = cur.fetchone()[0]
    
    return order_id

@app.route("/")
def index():
    list_products = sp_all_products()
    user = session.get('user')
    return render_template("index.html", list_products=list_products, user=user)

@app.route("/product/<int:product_id>")
def product(product_id):
    cur = con.cursor()
    cur.callproc("get_product_by_id", [product_id])
    selected_product = cur.fetchall()
    return render_template("product.html", product_id=product_id, selected_product=selected_product)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_form", methods=["POST"])
def login_form():
    email = request.form["email"]
    password = request.form["password"]

    cur = con.cursor()
    cur.callproc("check_account", [email, password])
    account = cur.fetchall()

    if account:
        session['user'] = account[0]
        return redirect(url_for("index"))
    else:
        flash("Invalid credentials, please try again.")
        return redirect(url_for("login"))

@app.route("/user_profile")
def user_profile():
    user = session.get('user')
    if user is None:
        return redirect(url_for("login"))
    return render_template("user_profile.html", user=user)

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for("index"))

@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    user = session.get('user')
    if not user:
        flash("You need to be logged in to add items to the cart")
        return redirect(url_for("login"))
    
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

@app.route("/cart")
def cart():
    user = session.get('user')

    if user:
        order_id = check_order_status()

        if order_id:
            cur = con.cursor()
            cur.execute("SELECT * FROM orders WHERE order_id=%s", order_id)
            user_order = cur.fetchall()
            return render_template("/cart.html", user=user, order_id=order_id, user_order=user_order)
        else:
            render_template("/cart.html", user=user)
            
    else:
        return render_template("/cart.html")

if __name__ == "__main__":
    secret_key = os.getenv("SECRET_KEY")
    app.secret_key = secret_key
    app.run(debug=True)
