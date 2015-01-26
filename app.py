from flask import Flask,request,url_for,redirect,render_template, flash, session
import json
from functools import wraps
import db_helper as db
import yelp
try:
    import urllib.request as urllib2
    import urllib.parse as urllib
except ImportError:
    import urllib2
    import urllib

app=Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

global orderid

@app.route("/", methods = ["POST", "GET"])
def index():
    return render_template ("index.html")

@app.route("/login", methods = ["POST", "GET"])
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
            return redirect("/profile")
        flash ("Invalid Username or Password")
        return redirect ("/")
    return render_template ("login.html")

@app.route("/register", methods = ["POST", "GET"])
def register():
    if (session.get('username') != None):
        flash ("You are already logged in!")
        return redirect ("/profile")
    register = request.args.get("register")
    if (register == "Register"):
        username = request.args.get("username")
        password = request.args.get("password")
        does_account_exist = db.user_auth(username, password);
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

@app.route("/profile", methods = ["POST", "GET"])
def profile():
    if ('username' in session):
        username = session ['username']
        return render_template ("profile.html", username = username, frees = db.get_data (username, frees), lunch = db.get_data (username, lunch), rep = db.get_data (username, rep), ordersp = db.get_data (username, ordersplaced), ordersf = db.get_data (username, ordersfulfilled), comments = db.get_data (username, comments));
    else:
        return redirect ("/login")

@app.route("/oprofile", methods = ["POST", "GET"])
def otherprofile(username): ##links from other user
    return render_template ("profile.html", username = username, frees = db.get_data (username, frees), lunch = db.get_data (username, lunch), rep = db.get_data (username, rep), ordersp = db.get_data (username, ordersplaced), ordersf = db.get_data (username, ordersfulfilled), comments = db.get_data (username, comments));

@app.route("/placeorder", methods = ["POST", "GET"])
def placeorder():
    submit = request.args.get("submit")
    if (submit == "Submit"):
        username = request.args.get("username")
        orderid = orderid + 1
        store = request.args.get("store")
        cost = request.args.get("cost")
        offer = request.args.get("offer")
        period1 = request.args.get("period1")
        period2 = request.args.get("period2")
        instruction = request.args.get("instruction")
        db.order_creat(orderid, username, store, food, cost, offer, period1, period2, instruction)
        return redirect ("/success")
    if ('username' in session):
        username = session ['username']
        return render_template ("placeorder.html", username = username);
    else:
        return render_template ("/login")
           
@app.route("/orders", methods=["POST", "GET"])
def loadorder():
    return render_template ("loadorder.html")

@app.route("/orderspec", methods=["POST", "GET"])
def specorder(stores, periods): ## one is null or not
    orders = get_orders (stores, period)
    return render_template ("specorder.html", orders);

@app.route("/results", methods=["POST", "GET"])
def results():
    search = request.args.get("search");

    if(search):
        term = request.args.get("term");
        loc = request.args.get("loc");
        results = yelp.search("restaurant","New York");
        if(results==None):
            flash("No results came up")
        return render_template ("results.html",results=results)
    else:
        return render_template("results.html", results=None)


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0')
