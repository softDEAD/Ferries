from flask import Flask,request,url_for,redirect,render_template, flash, session
import json, urllib2
from functools import wraps
import db_helper as db

app=Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'## will change to something more random

global orderid

@app.route("/", methods ["POST", "GET"])
def index():
    return render_template ("index.html")

@app.route("/login", methods ["POST", "GET"])
def login():
    if ('username' not in session):
        session ['username'] = None
    if (session.get('username') != None):
        flash ("You are already logged in!")
        return redirect("/")
    session ['username'] = None
    submit = request.args.get("submit")
    if (submit == "Submit"):
        username = request.args.get("username")
        password = request.args.get("password")
        does_account_exist = db.user_auth(username, password);
        if (does_account_exist == True):
            user = db.get_data (username);
            session ['username'] = username
            return redirect("/profile")
        flash ("Invalid Username or Password")
        return redirect ("/")
    return render_template ("login.html")

@app.route("/register", methods ["POST", "GET"])
def register():
    if (session.get('username') != None):
        flash ("You are already logged in!")
        return redirect ("/profile")
    register = request.args.get("register")
    if (register == "Register"):
        username = request.args.get("username")
        password = request.args.get("password")
        does_account_exist = user_auth(username, password);
        if (does_account_exist == True):
            flash("Account already exists") #tried registering with taken username (None, None) is not a valid user/pass combo
            return redirect("/register")
        elif (len(username)<6):
            flash("Username too short, must be at least 6 characters") #username too short, None falls under here too
            return redirect("/register")
        else:
            db.user_creat (username, password);
            flash("Successfully registered")
            return redirect ("/")
    return render_template ("register.html") #have a button that redirects to /

@app.route("/homepage")
def homepage ():
    if ('username' not in session):
        username = None
    if (session.get('username') != None):
        username = session ['username']
        
    search = request.args.get ("search")
    if (search != None):
        types = request.args.get ("types")
        if (types == "username")

        if (


    return render_template ("homepage.html")
        
@app.route("/profile", methods ["POST", "GET"])
def profile():
    if ('username' in session):
        data = db.get_all_user_data (username)
        return render_template ("profile.html", data=data)
    else:
        return redirect ("/login")

@app.route("/oprofile", methods ["POST", "GET"])
def otherprofile(username): ##links from other user
    data = db.get_all_user_data (username)
    return render_template ("profile.html", data = data)

@app.route("/placeorder", methods ["POST", "GET"])
def placeorder():
    submit = request.args.get("submit")
    if (submit == "Submit"):
        username = session ['username']
        orderid = orderid + 1
        store = request.args.get("store")
        cost = request.args.get("cost")
        offer = request.args.get("offer")
        period1 = request.args.get("period1")
        period2 = request.args.get("period2")
        instruction = request.args.get("instruction")
        db.order_creat(orderid, username, store, food, cost, offer, period1, period2, instruction) ## need error checking here
        return redirect ("/success")
    if ('username' in session):
        username = session ['username']
        return render_template ("placeorder.html", username = username);
    else:
        return render_template ("/login")
           

@app.route("/searchorder", methods ["POST", "GET"])
def searchorder(stores, periods): ## one is null or not
    orders = db.get_orders (stores, period)
    ret = []
    for s in orders:
        ret.append(db.get_all_order_data(s))
    return render_template ("searchorder.html", ret = ret) ## lists of list of orders
    
@app.route ("/success")
def success():
    return render_template ("success.html")

@app.route ("/yelp")
def yelp ():
    return render_template("yelp.html")


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0')
