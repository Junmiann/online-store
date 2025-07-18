from models.userOrder import UserOrder
from utils import *

class Cart:
    @staticmethod
    def cart_is_empty(con, order_id):
        """
        Check if cart is empty
        """
        user_orders_details = UserOrder.get_user_order_details(con, order_id)
        order_sum = user_orders_details[0][2]
        return order_sum == 0

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
    def get_stock_and_cart_quantity(con, order_id, product_id):
        with con.cursor() as cur:
            cur.callproc("get_product_by_id", [product_id])
            product = cur.fetchone()
            left_in_stock = product[6]
            
            cur.callproc("check_product_in_cart", [order_id, product_id])
            product_in_cart = cur.fetchall()
            return left_in_stock, product_in_cart

    @staticmethod
    def quantity_stock_comparison(con, user, user_chosen_quantity, order_id, product_id):
        """
        Compares the user's selected quantity with available stock
        If the quantity exceeds the available stock, an error is handled
        """
        left_in_stock, product_in_cart = Cart.get_stock_and_cart_quantity(con, order_id, product_id)
        cur = con.cursor()

        if user_chosen_quantity > left_in_stock:
            return False
        elif product_in_cart:
            product_quantity_in_cart = product_in_cart[0][3]
            if product_quantity_in_cart + user_chosen_quantity > left_in_stock:
                return False
            else:
                cur.callproc("update_cart_product_quantity", [user_chosen_quantity, order_id, product_id])
        else:
            cur.callproc("add_product", [order_id, user[0], product_id, user_chosen_quantity])

        return True
    
    @staticmethod
    def validate_and_update_cart_item_stock(con, order_id):
        with con.cursor() as cur:
            user_cart_items = Cart.get_cart_products(con, order_id)

            for item in user_cart_items:
                product_id = item[4]
                user_chosen_quantity = item[2]

                cur.callproc("get_product_by_id", [product_id])
                product = cur.fetchone()
                product_name = product[1]
                left_in_stock = product[6]

                if left_in_stock == 0:
                    handle_stock_error(con, f"{product_name} is unfortunately out of stock!", "cart.cart")
                    return False

                elif user_chosen_quantity > left_in_stock:
                    handle_stock_error(con, f"The quantity you selected for {product_name} exceeds our current stock.", "cart.cart")
                    return False

                cur.callproc("update_product_quantity", [product_id, user_chosen_quantity])

            return True
    
    @staticmethod
    def update_total_price(con, order_id):
        with con.cursor() as cur:
            cur.callproc("update_order_total_price", [order_id])
            con.commit()
            cur.close()
    
    @staticmethod
    def delete_product(con, order_id, product_id):
        with con.cursor() as cur:
            cur.callproc("delete_product", [order_id, product_id])
            con.commit()