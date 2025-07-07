class Cart:
    @staticmethod
    def get_product(con, product_id):
        """
        Get information about the product from cart
        """
        with con.cursor() as cur:
            cur.callproc("get_product_by_id", [product_id])
            cur.fetchall()
    
    @staticmethod
    def get_cart_products(con, order_id):
        """
        Each product's information (product name, quantity, sum) in the cart
        """
        with con.cursor() as cur:
            cur.callproc("get_cart_products", [order_id])
            cart_products = cur.fetchall()
            return cart_products
    
    @staticmethod
    def delete_product(con, order_id, product_id):
        with con.cursor() as cur:
            cur.callproc("delete_product", [order_id, product_id])
            con.commit()
    
    @staticmethod
    def check_out(con, user_id, order_id):
        with con.cursor() as cur:
            cur.callproc("order_check_out", [user_id, order_id])
            con.commit()

            cur.callproc("copy_cart_to_order_items", [order_id])
            con.commit()