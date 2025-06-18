from flask import Flask, render_template, session
from db import *
from routes import *
from utils import *

app = Flask(__name__)

order_id = None

register_blueprints(app)

@app.route("/")
def index():
    list_products = all_products()
    user = session.get("user")
    return render_template("index.html", list_products=list_products, user=user)

if __name__ == "__main__":
    secret_key = os.getenv("SECRET_KEY")
    app.secret_key = secret_key
    app.run(debug=True)
