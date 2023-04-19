from models import User, Product
from flask import Flask,request,jsonify,redirect,render_template, url_for, flash, session
from neo4j import GraphDatabase
from py2neo import Graph, Node, Relationship
import os
#driver=GraphDatabase.driver(uri=uri,auth=(username,pwd))
#session=driver.session()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
@app.route('/')
def home():
    lists = Product.getAll()
    return render_template('index.html',products=lists)
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        print(session.get('username'))
        flash('Logged in.')
        return render_template('index.html', username=username)
    return render_template('login.html')
@app.route('/signup')
def signup():
    return render_template('signup.html')
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
    app.run(debug=True)