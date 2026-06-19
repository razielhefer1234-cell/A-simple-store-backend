import random
import logging
import secrets
import string
from datetime import datetime
import hashlib
from System import User_Creation
from System import Login
from System import ProductStore
from System import Shopping_Cart

login = Login()
productstore = ProductStore()
shopping_cart = Shopping_Cart()

def menu():

    print("---Hello and welcome to our store---")
    print("Pls create an account and enter the following details:")
    print("""Username
Password""")

def sign_up():

    username = input("Pls enter a username: ")
    password = input("Pls enter a password: ")
    user = User_Creation(username, password)
    result = user.valid()
    return result

def log_in():

    print("Pls enter your username and password to log in:")
    username = input("Username: ")
    password = input("Password: ")
    result = login.login(username, password) 
    return result   

def log_menu():
    print("Pls pick from the followin options(pls pick a number):")
    print("1. Logout")
    print("2. Get product info")
    print("3. Add product to the store")
    print("4. Remove roduct from the store")
    print("5. Add product to your cart")
    print("6. Remove product from the cart")
    print("7. View your total")
    print("8. Checkout")
    print("9. End the program")
    
def choose():

    try:
        choose1 = int(input("Choose an option: "))
        return choose1
    except ValueError:
        print("Pls try a number 1 - 9 according to the menu")
        return choose()

def options(choose1):

    if choose1 == 1:
        username = input("Pls enter your username to logout: ")
        login.logout(username)
        return True
    elif choose1 == 2:
        product_name = input("Pls enter the product name: ")
        productstore.get_product(product_name)
        return True
    elif choose1 == 3:
        username = input("Pls enter your username: ")
        product_id = input("Pls enter the product id: ")
        product_name1 = input("Pls enter the product name: ")
        product_price = float(input("Pls input the product price: "))
        product_stock = int(input("Pls enter the product stock: "))
        productstore.add_product(username, product_id, product_name1, product_price, product_stock)
        return True
    elif choose1 == 4:
        username = input("Pls enter your username: ")
        product_name1 = input("Pls enter the product name: ")
        productstore.remove_products(username, product_name1)
        return True
    elif choose1 == 5:
        product_name1_2 = input("Pls enter the product name: ")
        shopping_cart.add_items(product_name1_2)
        return True
    elif choose1 == 6:
        product_name1_3 = input("Pls enter the product name: ")
        shopping_cart.remove_item(product_name1_3)
        return True
    elif choose1 == 7:
        shopping_cart.view_total()
        return True
    elif choose1 == 8:
        shopping_cart.checkout()
        return True
    elif choose1 == 9:
        print("The program has ended")
        return False
    else:
        print("Invalid option, please choose a number from 1 to 9.")
        return True

def run():
    menu()
    while not sign_up():
        print("Sign up failed, please try again.")

    if not log_in():
        return

    while True:
        log_menu()
        choice = choose()
        try:
            if not options(choice):
                break
        except ValueError as error:
            print(error)

run()




