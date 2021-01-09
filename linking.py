from flask import Flask, render_template, request
import sqlite3
import os


currentdirectory = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
@app.route("/")
def main():
    return render_template(r"index.html")

@app.route("/forward", methods = ["GET","POST"])
def forward():
    return render_template(r"home.html")

@app.route("/seller", methods = ["POST"])
def seller():
    return render_template(r"seller_login.html")
    
@app.route("/buyer", methods = ["POST"])
def buyer():
    return render_template(r"buyer_login.html")

@app.route("/seller_login", methods = ["POST"])
def seller_login():
    return render_template(r"seller_home.html")

@app.route("/buyer_login", methods = ["POST"])
def buyer_login():
    return render_template(r"buyer_home.html")

if __name__ == "__main__":
    app.run()