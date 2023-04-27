from models import User, Product
from flask import Flask,request,jsonify,redirect,render_template, url_for, flash, session
from neo4j import GraphDatabase
from py2neo import Graph, Node, Relationship
import os
#driver=GraphDatabase.driver(uri=uri,auth=(username,pwd))
#session=driver.session()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)


@app.route('/', methods=['GET','POST'])
def home():
    lists = Product.getAll()
    if session.get('username') is not None:
        print("------------------------------------------home-------------------------------------------------------")
        prod_id = request.form['id_pro']
        print(prod_id)
        allPro = Product.getAllID()
        p = None
        for item in allPro:
            print("item :" + str(item))
            if str(item) == prod_id:

                p = Product.getProduct(item)
                break

        print(p)
        user = session.get('username')
        u = User.getUserByName(session.get('username'))
        User.isLike(u, p)
        print('like')
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
        lists = Product.getAll()
        return render_template('index.html', username=username, products=lists)
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

@app.route('/productDetails/<int:prod_id>', methods=['GET','POST'])
def isLike(prod_id):
    if "username" not in session:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            p = Product.getProduct(prod_id)
            user = session.get('username')
            u = User.getUserByName(session.get('username'))
            User.addLike(u,p)
            return render_template('productDetails.html', prod=p)
        return render_template('productDetails.html', prod=Product.getProduct(prod_id), username=session.get('username') )


@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/productDetails/<int:prod_id>')
def productDetails(prod_id):
    p = Product.getProduct(prod_id)
    if session.get('username') is not None:
        print("------------------------------------------Detail-------------------------------------------------------")
        prod_id = request.form['id_pro']
        print(prod_id)
        allPro = Product.getAllID()

        for item in allPro:
            print("item :" + str(item))
            if str(item) == prod_id:
                p = Product.getProduct(item)
                break

        print(p)
        user = session.get('username')
        u = User.getUserByName(session.get('username'))
        User.isLike(u, p)
        print('like')
        return render_template('index.html', prod=p, username=session.get('username'))
    else:
        return render_template('productDetails.html', prod=p)



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
    app.run(debug=True, port=5001)