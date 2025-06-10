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
    def delete_product(con, order_id, product_id):
        with con.cursor() as cur:
            cur.callproc("delete_product", [order_id, product_id])
            con.commit()
    
    @staticmethod
    def check_out(con, user_id, order_id):
        with con.cursor() as cur:
            cur.callproc("order_check_out", [user_id, order_id])
            con.commit()