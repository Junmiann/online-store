import psycopg2
from psycopg2 import Error
from flask import Flask, render_template, flash, redirect, url_for, request
import os

app = Flask(__name__)

DB_HOST = os.getenv("PG_HOST")
DB_NAME = os.getenv("PG_DATABASE")
DB_USER = os.getenv("PG_USER")
DB_PASS = os.getenv("PG_PASSWORD")

con = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)

user = None
orderid = None

def sp_all_products():
    cur = con.cursor()

    cur.callproc("PUBLIC.sp_all_products")

    list_products = cur.fetchall()

    cur.close()

    return list_products

@app.route("/")
def index():
    list_products = sp_all_products()

    return render_template("index.html", list_products=list_products)

@app.route("/product/<int:product_id>")
def product(product_id):
    cur = con.cursor()

    cur.callproc("get_product_by_id", [product_id])

    selected_product = cur.fetchall()

    return render_template("product.html", product_id=product_id, selected_product=selected_product)

if __name__ == "__main__":
    secret_key = os.getenv("SECRET_KEY")
    app.secret_key=secret_key
    app.run(debug=True)