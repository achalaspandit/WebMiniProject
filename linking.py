import os
import sqlite3

import app as app
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploadImage'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# currentdirectory = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/SELLER-SIGN-IN")
def signin():
    return render_template('seller_login.html')


@app.route("/BUYER-SIGN-IN")
def buyer_signin():
    return render_template('buyer_login.html')


@app.route("/SELLER-SIGN-UP")
def signup():
    return render_template("seller_signup.html")


@app.route("/BUYER-SIGN-UP")
def buyer_signup():
    return render_template("buyer_signup.html")


@app.route("/forward", methods=["GET", "POST"])
def forward():
    return render_template("home.html")


@app.route("/seller", methods=["POST"])
def seller():
    return render_template("seller_login.html")


@app.route("/seller_login", methods=["POST"])
def seller_login():
    if request.method == 'POST':
        try:
            sellerid = request.form['SellerId']
            password = request.form['sellerpassword']
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                found = 0
                for row in cur.execute("SELECT sellerId, password from seller_login"):
                    id = row[0]
                    pwd = row[1]
                    if id == sellerid and pwd == password:
                        msg = "Logged in"
                        found = 1
                        break
                    if found == 0:
                        msg = "Try again, Enter Valid Credentials"
                        return render_template("success.html", msg=msg)
        except:
            con.rollback()
            msg = "Error, Enter Valid Credentials"
            return render_template("success.html", msg=msg)
        finally:
            if found == 1:
                return render_template("seller_home.html")
            con.close()


@app.route("/seller_signup", methods=["POST"])
def seller_signup():
    if request.method == 'POST':
        try:
            sellerId = request.form['sellerID']
            seller_name = request.form['sellername']
            password = request.form['sellerpassword']
            gstin = request.form['gstid']
            mobile_no = request.form['sellernumber']
            pregex = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
            mregex = '^((\+)?(\d{2}[-]))?(\d{10}){1}?$'
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO sellerSignup(sellerId,seller_name,password,gstin,mobile_no) VALUES (?,?,?,?,?)",
                    (sellerId, seller_name, password, gstin, mobile_no))
                con.commit()
                msg = "Record successfully added, Login to continue"
                return render_template("success.html", msg=msg)
        except:
            con.rollback()
            msg = "Error in insert operation, Try again"
            return render_template("try_again.html", msg=msg)
        finally:

            con.close()


@app.route("/buyer_signup", methods=["POST"])
def buyer_signup1():
    if request.method == 'POST':
        try:
            buyerId = request.form['buyerID']
            buyer_name = request.form['buyerusername']
            password = request.form['buyerpassword']
            mobile_no = request.form['buyernumber']
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO buyerSignup(buyerId,buyer_name,password,mobile_no) VALUES (?,?,?,?)",
                            (buyerId, buyer_name, password, mobile_no))
                con.commit()
                msg = "Record successfully added"
                return render_template("buyer_success.html", msg=msg)
        except:
            con.rollback()
            msg = "Error in insert operation, Try again"
            return render_template("buyer_try_again.html", msg=msg)
        finally:

            con.close()


@app.route("/sellorder", methods=["POST"])
def sellorder():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT buyer_name, buyer_address,Product_name,Product_id,Category_prod,quantity_buy from orders")
        data = cur.fetchall()
        for row in data:
            print(row[0], row[1], row[2], row[3], row[4], row[5])
    conn.close()
    return render_template("seller_orders.html", data=data)


# @app.route("/inventory", methods = ["POST"])
# def inventory():
#     return render_template("seller_inventory.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/seller_add_product", methods=["POST"])
def seller_add_product():
    print("hello")
    if request.method == 'POST':
        print("inisde")
        print("hiii")

        sellerId = request.form['SellerId']
        print("done1")
        prod_name = request.form['prod_name']
        prod_id = request.form['prod_id']
        category = request.form['category']
        quantity = request.form['quantity']
        print("done1")
        price = request.form['price']
        description = request.form['description']
        print("done1")
        image = request.files['image']
        print("uploaded")
        if image and allowed_file(image.filename):
            print("inside if")
            filename = secure_filename(image.filename)
            print("file name ", filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            print(path)
            image.save(path)
            print("saved path")
        imagename = filename
        print(imagename)

        with sqlite3.connect('database.db') as con:
            try:
                print('established')
                cur = con.cursor()
                print('database')
                # cur.execute('''INSERT INTO inventory(sellerId,Product_name,Product_id,Category_prod,quantity,image,price,Description) VALUES (?,?,?,?,?,?,?,?)''',
                #             (sellerId,prod_name,prod_id,category,quantity,imagename,price,description))
                print("added")
                for row in cur.execute("SELECT sellerId from seller_login"):
                    id = row[0]
                    if id == sellerId:
                        cur.execute(
                            '''INSERT INTO inventory(sellerId,Product_name,Product_id,Category_prod,quantity,image,price,Description) VALUES (?,?,?,?,?,?,?,?)''',
                            (sellerId, prod_name, prod_id, category, quantity, imagename, price, description))
                        msg = "Record successfully added"
                        return render_template("add_successfull.html", msg=msg)
                    else:
                        msg = "ID doesnt match, try again"
                        return render_template("add_failure.html", msg=msg)
                con.commit()


            except:
                con.rollback()
                msg = "Error in insert operation, try again"
                return render_template("add_failure.html", msg=msg)
                con.close()


@app.route("/addproduct", methods=["POST"])
def addproduct():
    return render_template("seller_add_product.html")


@app.route("/buyer", methods=["POST"])
def buyer():
    return render_template("buyer_login.html")


@app.route("/buyer_checkout")
def buyer_checkout():
    return render_template("buyer_Checkout.html")


@app.route("/buyer_login", methods=["POST"])
def buyer_login():
    if request.method == 'POST':
        try:
            buyerid = request.form['buyerId']
            password = request.form['password']
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                found = 0
                for row in cur.execute("SELECT buyerId, password from buyer_login"):
                    id = row[0]
                    pwd = row[1]
                    if id == buyerid and pwd == password:
                        msg = "Logged in"
                        found = 1
                        break
                if found == 0:
                    msg = "Try again, Enter Valid Credentials"
                    return render_template("buyer_loginFail.html", msg=msg)
        except:
            con.rollback()
            msg = "Error, Enter Valid Credentials"
            return render_template("buyer_loginFail.html", msg=msg)
        finally:
            if found == 1:
                return render_template("buyer_selection.html")
            con.close()


@app.route("/buyer_hand", methods=["POST"])
def buyer_hand():
    return render_template("buyer_handSelection.html")


@app.route("/buyer_text", methods=["POST"])
def buyer_text():
    return render_template("buyer_textSelection.html")


@app.route("/buyer_jewe", methods=["POST"])
def buyer_jewe():
    return render_template("buyer_jeweSelection.html")


@app.route("/buyer_cond", methods=["POST"])
def buyer_cond():
    return render_template("buyer_condSelection.html")


@app.route("/add")
def add_product_to_cart():
    return render_template("buyer_Checkout.html")


@app.route("/checkout")  # , methods = ["GET","POST"])
def checkout():
    # if request.method == 'POST':
    print("inside checkout")
    try:
        print("inside try")
        with sqlite3.connect('database.db') as con:
            print("database connected")
            cur = con.cursor()
            # words=[]
            cur.execute("SELECT Product_name,image,price,Description from inventory")
            print("selected")
            data = cur.fetchall()
            # for item in data:
            #     for row in item:
            #         words.append(row.split())
            print("data")

            return render_template("buyer_itemSelection", products=data)
    except:
        con.rollback()
        msg = "error"
    finally:
        print(data)
        con.close()


@app.route("/disp_inventory")  # , methods = ["GET","POST"])
def disp_inventory():
    # if request.method == 'POST':
    print("inside disp_inventory")
    try:
        print("inside try")
        with sqlite3.connect('database.db') as con:
            print("database connected")
            cur = con.cursor()
            cur.execute("SELECT Product_name,Category_prod, quantity, price, Description from inventory")
            print("selected")
            data = cur.fetchall()

            print(data)
            # return render_template("seller_inventory.html", data=data)
    except:
        con.rollback()
        msg = "error"
    finally:
        print(data)
        con.close()
    return render_template("seller_inventory.html", data=data)


@app.route("/card", methods=["POST"])
def card():
    return render_template("buyer_card_details.html")


@app.route("/previous")
def previous():
    return render_template("buyer_selection.html")


@app.route("/success")
def success():
    return render_template("buyer_paySucess.html")


@app.route("/gohome", methods=["POST"])
def gohome():
    return render_template("buyer_payUnsucessful.html")


if __name__ == "__main__":
    app.run()
