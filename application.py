import psycopg2
from psycopg2 import Error
from flask import Flask, render_template, flash, redirect, url_for, request, session
import os

app = Flask(__name__)

DB_HOST = os.getenv("PG_HOST")
DB_NAME = os.getenv("PG_DATABASE")
DB_USER = os.getenv("PG_USER")
DB_PASS = os.getenv("PG_PASSWORD")

con = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)

def sp_all_products():
    cur = con.cursor()
    cur.callproc("sp_all_products")
    list_products = cur.fetchall()
    cur.close()
    return list_products

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
    user = session.get('user')
    return render_template("product.html", product_id=product_id, selected_product=selected_product, user=user)

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
    return render_template("user_profile.html", user=user)

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    secret_key = os.getenv("SECRET_KEY")
    app.secret_key = secret_key
    app.run(debug=True)
