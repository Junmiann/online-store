import psycopg2
from psycopg2 import Error
from flask import Flask, render_template, flash, redirect, url_for, request
import os
from dotenv import load_dotenv
from datetime import date

app = Flask(__name__)

DB_HOST = os.getenv('PG_HOST')
DB_NAME = os.getenv('PG_DATABASE')
DB_USER = os.getenv('PG_USER')
DB_PASS = os.getenv('PG_PASSWORD')

con = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)

''' user and orderId is none when no ones logged in ''' 
user = None
orderid = None

''' all products '''
def all_products():
    cur = con.cursor()

    cur.execute("SELECT * FROM show_products ORDER BY product_id")

    list_products = cur.fetchall()

    list_products_with_id = []
    for product in list_products:
        product_with_id = list(product)
        product_with_id.append(product[0])
        list_products_with_id.append(tuple(product_with_id))

    cur.close()

    return list_products_with_id

''' startpage '''
@app.route("/")
def index():
    list_products = all_products()

    return render_template("index.html", list_products=list_products)

if __name__ == "__main__":
    secret_key = os.getenv('SECRET_KEY')
    app.secret_key=secret_key
    app.run(debug=True)