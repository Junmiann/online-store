from flask import session
from db import *

def sp_all_products():
    cur = con.cursor()
    cur.callproc("sp_all_products")
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