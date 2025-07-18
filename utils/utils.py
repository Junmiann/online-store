from flask import session, flash, redirect, url_for
from db import *

def all_products():
    cur = con.cursor()
    cur.callproc("all_products")
    list_products = cur.fetchall()
    cur.close()
    return list_products

def check_order_status():
    global order_id
    user = session.get("user")

    if user:
        cur = con.cursor()
        cur.callproc("check_order_status", [user[0], 'Pending'])
        order_status = cur.fetchone()

        if order_status:
            order_id = order_status
        else:
            cur.callproc("create_order", [0, user[0]])
            con.commit()
            order_id = cur.fetchone()[0]

        cur.close()
    
        return order_id
    else:
        return None
    
def handle_stock_error(con, message, endpoint, **url_params):
    con.rollback()
    flash(message)
    return redirect(url_for(endpoint, **url_params))