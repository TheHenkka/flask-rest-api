from flask import Flask, render_template, redirect, url_for, jsonify, request, session
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import sqlite3
import pathlib
import hashlib
import sys
import os

app = Flask(__name__)
app.secret_key = "verybadexample"
api = Api(app)  

#Checks and validates input arguments.
put_parser = reqparse.RequestParser()
put_parser.add_argument('items', type=str, required=True, help='Cannot save/update empty cart')
put_parser.add_argument('country', type=str, required=True, help='Country is required for VAT purposes')

update_parser = reqparse.RequestParser()
update_parser.add_argument('items', type=str, required=True, help='Cannot save/update empty cart')
update_parser.add_argument('country', type=str, help='Country is required for VAT purposes')

class CartView(Resource):

    #Find and return cart content using ID. Returns content as response. (Cart's items are just stored as JSON string to 'cart' table..)
    def get(self, id):

        cartExists = checkCart(id)
        if cartExists == False:
            abort(404, message="Cart {} doesn't exist".format(id))
        
        cart  = findCart(id)
        items = []
        itemIDlist = cart[0]['items'][1:-1].split(',')

        # Add all items from the cart to list based on ID.
        for i in itemIDlist:
            items.append(findItem(i)[0])

        cart[0]['items'] = items
        
        return jsonify(cart)

    # Not used
    def put(self,id):
        pass


    #Updates cart based on ID
    def patch(self, id):
        cartExists = checkCart(id)

        if cartExists == False:
            abort(404, message="Cart {} doesn't exist".format(id))

        args = update_parser.parse_args()
        country = args['country']
        items = args['items']

        if not args['country']:
            cart  = findCart(id)
            country = cart[0]['country']

        updateCart(items, country, id)

        return '', 200
        

    #Delete cart based on ID. 
    def delete(self,id):

        cartExists = checkCart(id)
        if cartExists ==True:
            try:
                deleteCart(id)
                return '', 204
            except:
                abort(404, message="Cart {} doesn't exist".format(id))
        else:
            return '', 304


class Cart(Resource):

    #Adds new cart to database. Returns ID as response.
    def put(self):

        args = put_parser.parse_args()
        newId = saveCart(args['items'], args['country'])

        return {'id':newId}

api.add_resource(CartView, '/cart/<int:id>')
api.add_resource(Cart, '/cart')


# Front page. Lists commands for API.
@app.route('/')
def index():
    return render_template('index.html')


# Admin page. Shows all the carts and their content.
@app.route('/admin')
def admin():

    if not 'admin' in session:
        return redirect(url_for('login'))

    carts = getCarts()

    return render_template('admin.html', carts = carts)


# Login page. Checks username and password. TODO: errors if login fails.
# USERNAME: admin 
# PASSWORD: root
@app.route('/login', methods=['POST','GET']) 
def login():

    if request.method == 'POST':
        try:
            username = request.form['username']
        except:
            username = ""
        try:
            password = request.form['password']
        except:
            password = ""
        
        m = hashlib.sha512()
        m.update(app.secret_key.encode('utf-8'))
        m.update(password.encode('utf-8'))

        if username == "admin" and m.digest() == b"\x81\x85\xa0z\xfd\xb4\x07\x9b\xc4\x8c?A\x01\xdd\xc4\xfb\xcc7\x8fB\xfa\xd9e\xa5l\xd9\xf7G\xca\xaf\xfc4\xf7\x87\xf4\x94\xdd\xb1\xd7\xaa\x10T\xcd\x7f~>\xbb=\x94\xc7\x95oxcn\xb9\x81\xcdA\xe9\xc1\xf7\x9c2":
            session['admin'] = username
            return redirect(url_for('admin'))

    return render_template('login.html')

# Logs user out and redirects to main page. TODO: logout button.
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))


# Open the database
def openData():
    try:
        con = sqlite3.connect(pathlib.Path('database.sql'))
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")
        return con
    except:
        print("Can't open Database")
        for err in sys.exc_info():
            print(err)
        return None


# Finds cart
def findCart(id):

    find = """ SELECT *
			FROM cart
            WHERE id = :id 
			"""

    con = openData()
    cur = con.cursor()
    cart =[]

    try:
        cur.execute(find, {"id":id})
        for row in cur.fetchall():
            cart.append({'cart_id': row[0], 'items': row[1], 'country': row[2]})
    except:
        print("Can't find in DB, error: {0}".format(sys.exc_info()))

    return cart


# Check if cart exists
def checkCart(id):

    find = """ SELECT 1
			FROM cart
            WHERE id = :id 
			"""

    con = openData()
    cur = con.cursor()
    exists = False

    try:
        cur.execute(find, {"id":id})
        for row in cur.fetchall():
            exists =True
    except:
        print("Can't find item in DB, error: {0}".format(sys.exc_info()))

    return exists


# Finds item
def findItem(id):

    find = """ SELECT *
			FROM item
            WHERE item_id = :id 
			"""

    con = openData()
    cur = con.cursor()
    itemList =[]

    try:
        cur.execute(find, {"id":id})
        for row in cur.fetchall():
            itemList.append({'id': row[0], 'name': row[1], 'price': row[2]})
    except:
        print("Can't find item in DB, error: {0}".format(sys.exc_info()))

    return itemList


# Save new cart to database and return its new ID.
def saveCart(items, country):

    add = """
            INSERT INTO cart (items, country)
            VALUES (:items, :country)
            """

    con = openData()
    cur = con.cursor()

    try:
        cur.execute(add, {"items": items, "country": country})
        con.commit()
        return cur.lastrowid
    except:
        print("Can't add to DB, error: {0}".format(sys.exc_info()))


# Delete cart from database
def deleteCart(id):

    delete = """
            DELETE FROM cart 
            WHERE id = :id 
            """
    con = openData()
    cur = con.cursor()

    try:
        cur.execute(delete, {"id": id})
        con.commit()
    except:
        print("Can't delete cart, error: {0}".format(sys.exc_info()))


# Get all the carts for admin page.
def getCarts():

    find = """ SELECT *
			FROM cart
			"""
    con = openData()
    cur = con.cursor()
    cartList =[]

    try:
        cur.execute(find)
        for row in cur.fetchall():
            cartList.append({'id': row[0], 'items': row[1], 'country': row[2]})
    except:
        print("Can't find item in DB, error: {0}".format(sys.exc_info()))

    return cartList

def updateCart(items, country, id):

    update= """UPDATE cart
                SET items = :items, country = :country
                WHERE id = :id
                """

    con = openData()
    cur = con.cursor()

    try:
        cur.execute(update, {"items": items, "country": country, "id": id})
        con.commit()
    except:
        print("Can't update cart in DB, error: {0}".format(sys.exc_info()))

#Debugging help
if __name__ == "__main__":
    app.run(debug=True)