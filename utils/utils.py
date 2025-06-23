from flask import session
from db import *

def all_products():
    cur = con.cursor()
    cur.callproc("all_products")
    list_products = cur.fetchall()
    cur.close()
    return list_products

def user_details():
    user = session.get("user")
    
    user_id = user[0]
    user_name = user[1]
    user_email = user[4]
    is_admin = user[9]
    return user_id, user_name, user_email, is_admin

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