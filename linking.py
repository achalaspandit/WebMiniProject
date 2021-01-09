from flask import Flask, render_template, request
import sqlite3
import os


currentdirectory = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
@app.route("/")
def main():
    return render_template("index.html")

@app.route("/forward", methods = ["GET","POST"])
def forward():
    return render_template("home.html")

@app.route("/seller", methods = ["POST"])
def seller():
    return render_template("seller_login.html")

@app.route("/seller_login", methods = ["POST"])
def seller_login():
    return render_template("seller_home.html")
    
@app.route("/sellorder", methods = ["POST"])
def sellorder():
    return render_template("seller_orders.html")

@app.route("/inventory", methods = ["POST"])
def inventory():
    return render_template("seller_inventory.html") 

@app.route("/addproduct", methods = ["POST"])
def addproduct():
    return render_template("seller_add_product.html") 

    
@app.route("/buyer", methods = ["POST"])
def buyer():
    return render_template("buyer_login.html")

@app.route("/buyer_login", methods = ["POST"])
def buyer_login():
    return render_template("buyer_selection.html")

@app.route("/buyer_item", methods = ["POST"])
def buyer_item():
    return render_template("buyer_itemSelection.html")

@app.route("/checkout", methods = ["POST"])
def checkout():
    return render_template("buyer_Checkout.html")

@app.route("/card", methods = ["POST"])
def card():
    return render_template("buyer_card_details.html")

@app.route("/previous", methods = ["POST"])
def previous():
    return render_template("buyer_selection.html")

@app.route("/gohome", methods = ["POST"])
def gohome():
    return render_template("buyer_payUnsucessful.html")  

if __name__ == "__main__":
    app.run()