from flask import Flask, render_template, redirect, url_for, session
from db import *
from routes import *
from utils import *

app = Flask(__name__)

order_id = None

register_blueprints(app)

@app.route("/")
def index():
    user = session.get("user")
    if user is None or user[9] == False:
        list_products = all_products()
        return render_template("index.html", list_products=list_products, user=user)
    elif user[9]:
        return redirect(url_for("admin_dashboard.admin_dashboard", section="orders"))

if __name__ == "__main__":
    secret_key = os.getenv("SECRET_KEY")
    app.secret_key = secret_key
    app.run(debug=True)
