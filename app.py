from models import User, Product
from flask import Flask,request,jsonify,redirect,render_template, url_for, flash, session
from neo4j import GraphDatabase
from py2neo import Graph, Node, Relationship
import os
import models
#driver=GraphDatabase.driver(uri=uri,auth=(username,pwd))
#session=driver.session()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)


@app.route('/')
def home():
    lists = Product.getAll()
    if session.get('username') is not None:
        return render_template('index.html', products=lists, username=session.get('username'))
    else:
        return render_template('index.html', products=lists)
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        print(session.get('username'))
        flash('Logged in.')
        return redirect(url_for('home'))
        #return render_template('index.html', username=username)
    return render_template('login.html')


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        sexe = request.form['sexe']
        birth = request.form['birth']
        User(username).register(fullname, sexe, birth, password)

        flash('Logged in.')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/cart')
def cart():
    if "cart" not in session:
        flash("There is nothing in your cart.")
        return render_template("cart.html", display_cart={}, total=0)
    else:
        items = session["cart"]
        dict_of_prod = {}
        total_price = 0
        for id in items:
            product = models.getProdByID(id)
            total_price += product['price']
            dict_of_prod[product['id']] = {"name": product['name'], "price": product['price']}

        return render_template("cart.html", display_cart=dict_of_prod, total=total_price)

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    if "cart" not in session:
        session["cart"] = []
    if id not in session["cart"]:
        session["cart"].append(id)

    flash("Successfully added to cart!")
    return redirect("/cart")

@app.route('/buy')
def confirmCart():
    if "username" not in session:
        return redirect(url_for('login'))
    else:
        items = session["cart"]
        user = models.getUserByName(session.get('username'))
        for id in items:
            product = models.getProdByID(id)
            models.addRelBuy(user,product)
        session.pop('cart', None)
        return redirect(url_for('home'))

@app.route('/likeProduct/<int:prod_id>', methods=['GET','POST'])
def isLike(prod_id):
    if "username" not in session:
        return redirect(url_for('login'))
    else:
        p = models.getProdByID(prod_id)
        print("***************prod",p)
        user = session.get('username')
        u = models.getUserByName(session.get('username'))
        print("***************user", u)
        models.addLike(u,p)
        return redirect(url_for('home'))


@app.route('/productDetails/<int:prod_id>')
def productDetails(prod_id):
    p = Product.getProduct(prod_id)
    return render_template('productDetails.html', prod=p)
if __name__ == "__main__":
    app.run(debug=True, port=5000)