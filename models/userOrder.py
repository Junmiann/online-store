class UserOrder:
    @staticmethod
    def get_user_orders(con, user):
        """
        All of the customer's orders (order ID, date, total sum, status)
        """ 
        with con.cursor() as cur:
            cur.callproc("customer_orders", [user])
            user_orders = cur.fetchall()
            return user_orders
    
    @staticmethod
    def get_user_order_details(con, order_id):
        """
        Customer's specific order details (order ID, order date, total sum)
        """
        with con.cursor() as cur:
            cur = con.cursor()
            cur.callproc("get_order_details", [order_id])
            user_order_details = cur.fetchall()
            return user_order_details
    
    @staticmethod
    def get_user_order_products(con, order_id):
        """
        Each product's information (product name, quantity, sum) in the order
        """
        with con.cursor() as cur:
            cur.callproc("get_order_products", [order_id])
            user_order_products = cur.fetchall()
            return user_order_products
        
    @staticmethod
    def check_out(con, user_id, order_id):
        with con.cursor() as cur:
            cur.callproc("order_check_out", [user_id, order_id])
            con.commit()

            cur.callproc("copy_cart_to_order_items", [order_id])
            con.commit()