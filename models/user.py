from werkzeug.security import generate_password_hash

class User:
    def __init__(self, firstname, lastname, email, password, phone, address, city, country):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email.strip().lower()
        self.password_hash = generate_password_hash(password)
        self.phone = phone
        self.address = address
        self.city = city
        self.country = country
    
    def save_user_to_db(self, con):
        with con.cursor() as cur:
            cur.callproc("register_account", [
                self.firstname, self.lastname, self.email, self.password_hash,
                self.phone, self.address, self.city, self.country
            ])
            con.commit()