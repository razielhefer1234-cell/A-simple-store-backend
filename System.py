import random
import logging
import secrets
import string
from datetime import datetime
import hashlib

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("Store.log"),
    ]
)


user_data_base = {}

products = {}

class User_Creation:

    def __init__(self, username, password):
        
        self.logger = logging.getLogger(self.__class__.__name__)
        self.username = username
        self.password = password
        self.id = secrets.token_hex(12)
        self.date = datetime.now()
        self.errors = []

    def _username(self):

        valid = True

        if self.username in user_data_base:
            self.errors.append("Username is already taken pls try again")
            self.logger.error("Username is already taken pls try again")
            valid = False
        
        if " " in self.username:
            self.errors.append("Username can't have blank spaces")
            self.logger.error("Username can't have blank spaces")
            valid = False
        
        if len(self.username) < 4:
            self.errors.append("Username must contain more then 3 letters")
            self.logger.error("Username must contain more then 3 letters")
            valid = False
        
        return valid

    def _check_password(self):

        valid = True

        if len(self.password) < 8 or len(self.password) > 16:
            self.errors.append("Password must be bettwen 8 - 16 characters long")
            self.logger.error("Password must be bettwen 8 - 16 characters long")
            valid = False

        if any(i == " " for i in self.password):
            self.errors.append("Password can't contain black spaces")
            self.logger.error("Password can't contain black spaces")
            valid = False

        if not any(i.isupper() for i in self.password):
            self.errors.append("Password must contain one upper letteral least")
            self.logger.error("Password must contain one upper letteral least")
            valid = False

        if not any(i.islower() for i in self.password):
            self.errors.append("Password must contain one lower letteral least")
            self.logger.error("Password must contain one lower letteral least")
            valid = False

        if all(i not in self.password for i in str(string.digits)):
            self.errors.append("Password must contain at least one number")
            self.logger.error("Password must contain at least one number")
            valid = False

        if all(i not in self.password for i in string.punctuation):
            self.errors.append("Password must contain at least one special character")
            self.logger.error("Password must contain at least one special character")  
            valid = False
        
        return valid
    
    def status(self):

        return "Manager" if self.password == "Store_Manager1234@" else "Customer"
    
    def valid(self):

        username_ok = self._username()
        password_ok = self._check_password()

        if username_ok and password_ok:
            self.logger.info(f"Storing {self.username} in the user data base")
            user_data_base[self.username] = {
                "Id": self.id,
                "Password": hashlib.sha256(self.password.encode()).hexdigest(),
                "Status": self.status(),
                "Date of creation": self.date,
                "Failed login": 0,
                "Blocked": False,
                "Login": False
            }
            self.password = None
            return True
        
        for i in self.errors:
            print(i)
        return False
    
class Login:
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def login(self, username, password):

        if username not in user_data_base:
            raise ValueError(f"{username} not in the  user data base")
            self.logger.error(f"{username} not in the  user data base")
        
        if user_data_base[username]["Blocked"]:
            self.logger.error(f"{username} is blocked")
            raise ValueError(f"{username} is blocked")

        if user_data_base[username]["Failed login"] >= 3:
            user_data_base[username]["Blocked"] = True
            self.logger.error(f"{username} is now blocked")
            raise ValueError(f"{username} is now blocked")

        if hashlib.sha256(password.encode()).hexdigest() != user_data_base[username]["Password"]:
            user_data_base[username]["Failed login"] += 1
            self.logger.error("Password is not correct")
            raise ValueError("Password is not correct")
        
        user_data_base[username]["Failed login"] = 0
        user_data_base[username]["Login"] = True
        print("You're now logged in")
        self.logger.info("You're now logged in")
        return True
    
    def logout(self, username):
        if username not in user_data_base:
            raise ValueError(f"{username} not in the  user data base")
            self.logger.error(f"{username} not in the  user data base")
        
        if user_data_base[username]["Blocked"]:
            raise ValueError(f"{username} is blocked")
            self.logger.error(f"{username} is blocked")
        
        user_data_base[username]["Login"] = False
        print("You're now logged out")
        self.logger.info("You're now logged out")
        return True

class ProductStore:

    def __init__(self):
        
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_product(self, product_name):
        for product in products.values():
            if product["Name"] == product_name:
                print(f"Id: {product['Id']}, Name: {product['Name']}, Price: {product['Price']}, Stock: {product['Stock']}")
                self.logger.info(f"Product found: {product}")
                return True
        self.logger.error("Product not in the data base")
        raise ValueError("Product not in the data base")
    
    def add_product(self, username, product_id, product_name, price, stock):
        
        if username not in user_data_base:
            self.logger.error(f"{username} not in the user data base")
            raise ValueError(f"{username} not in the user data base")

        if user_data_base[username]["Status"] != "Manager":
            self.logger.error("To add products you need to be a Manager")
            raise ValueError("To add products you need to be a Manager")

        if product_name in products:
            self.logger.error("Product already in the data base")
            raise ValueError("Product already in the data base")
        
        products[product_name] = {
            "Id": product_id,
            "Name": product_name,
            "Price": price,
            "Stock": stock
        }
        print("Product added successfully")
        self.logger.info("Product added successfully")
        return True
    
    def remove_products(self, username, product_name):
        
        if username not in user_data_base:
            self.logger.error(f"{username} not in the user data base")
            raise ValueError(f"{username} not in the user data base")

        if user_data_base[username]["Status"] != "Manager":
            self.logger.error("To remove products you need to be a Manager")
            raise ValueError("To remove products you need to be a Manager")

        if product_name not in products:
            self.logger.error("Product not in the data base")
            raise ValueError("Product not in the data base")
        
        del products[product_name]
        print("Product removed successfully")
        self.logger.info("Product removed successfully")
        return True
    
class  Shopping_Cart:

    def __init__(self):
        
        self.logger = logging.getLogger(self.__class__.__name__)
        self.cart = []
    
    def add_items(self, productname):

        for i in products.values():
            if i["Name"] == productname:
                if i["Stock"] == 0:
                    raise ValueError(f"There is no {i['Name']} left in stock")
                    self.logger.error(f"There is no {i['Name']} left in stock")
                    return False
                i["Stock"] -= 1
                self.cart.append(productname)
                print("Product was added successfully")
                self.logger.info("Product was added successfully")
                return True
        raise ValueError("Product not in the data base")
        self.logger.error("Product not in the data base")
        return False

    def remove_item(self, productname):

        if productname not in self.cart:
            raise ValueError("Product not in cart")
            self.logger.error("Product not in cart")
            return False
        
        for i in products.values():
            if i["Name"] == productname:
                i["Stock"] += 1
        self.cart.remove(productname)
        print("Product was removed successfully")
        self.logger.info("Product was removed successfully")
        return True
    
    def view_total(self):
        
        total = 0

        for i in self.cart:
            for w in products.values():
                if i == w["Name"]:
                    total += w["Price"]
        print(f"Your total is {total:.2f}")
        self.logger.info(f"Your total is {total:.2f}")
        return True
    
    def checkout(self):
        
        total = 0

        for i in self.cart:
            for w in products.values():
                if i == w["Name"]:
                    total += w["Price"]
        print("Receipt")
        self.logger.info("Receipt")
        print(f"Time {datetime.now()}")
        self.logger.info(f"Time {datetime.now()}")

        for i in self.cart:
            for w in products.values():
                if i == w["Name"]:
                    print(f'{w["Name"]}: ${w["Price"]:.2f}')
                    self.logger.info(f'{w["Name"]}: ${w["Price"]:.2f}')
        
        print(f"Your total is {total}")
        self.logger.info(f"Your total is {total}")
        
        




