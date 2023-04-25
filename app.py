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
            dict_of_prod[product.identity] = {"name": product['name'], "price": product['price']}

        return render_template("cart.html", display_cart=dict_of_prod, total=total_price)

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(id)

    flash("Successfully added to cart!")
    return redirect("/cart")
'''
@app.route('/', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        User(username).register(password)
        session['username'] = username
        print(session.get('username'))
        flash('Logged in.')
        return redirect(url_for('welcome'))
    return render_template('index2.html')
@app.route('/welcome')
def welcome():
    username = session.get('username')
    return render_template('welcome.html', username=username)
@app.route("/display",methods=["GET","POST"])
def display_node():
    q1="""
    match (n) return n
    """
    results=session.run(q1)
    data=results.data()
    return(jsonify(data))'''
if __name__ == "__main__":
    app.run(debug=True, port=5000)