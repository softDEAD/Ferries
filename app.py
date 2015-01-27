from flask import Flask,request,url_for,redirect,render_template, flash, session
import json, urllib2
from functools import wraps
import db_helper as db
import yelp

app=Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

orderid = 0
id = 0

def search(func):
    @wraps(func)
    def inner(*args,**kwargs):
        select = request.args.get("select")
        search = request.args.get("search")
        searchsubmit = request.args.get("searchsubmit")
        if(searchsubmit == "Search"): 
            if (select == "Period"):
                orders = db.get_orders ([], [int(search)])
            elif (select == "Store"):
                orders = db.get_orders ([str(search)], [])
            else:
                return redirect("/profile/" + str(search))
            return render_template ("index.html", orderid = orderid, orders = orders);
        else:
            return func(*args,**kwargs)
    return inner

@app.route("/", methods = ["POST", "GET"])
@search
def index():
    global orderid
    if(request.method=="POST"):
        submit = request.form["submit"]
        if (submit == "Search"):
            return redirect("/results")
    if ('username' not in session or session.get('username') == None):
        loggedin = False
        return render_template ("index.html", loggedin = loggedin)
    else:
        loggedin = True
        username2 = session.get('username')
        return render_template ("index.html", orderid = orderid, loggedin = loggedin, username2 = username2)

@app.route("/login", methods = ["POST", "GET"])
@search
def login():
    if ('username' not in session):
        session ['username'] = None
    if (session.get('username') != None):
        flash ("You are already logged in!")
        return redirect("/profile/" + str (session.get('username')))
    session ['username'] = None
    submit = request.args.get("submit")
    if (submit == "Submit"):
        username = request.args.get("username")
        password = request.args.get("password")
        does_account_exist = db.user_auth(username, password);
        if (does_account_exist == True):
            user = db.get_all_user_data (username)
            session ['username'] = username
            return redirect("/profile/" + str (username))
        flash ("Invalid Username or Password")
        return redirect ("/")
    return render_template ("login.html")

@app.route("/register", methods = ["POST", "GET"])
@search
def register():
    if (session.get('username') != None):
        flash ("You are already logged in!")
        return redirect ("/profile")
    register = request.args.get("register")
    if (register == "Register"):
        username = request.args.get("username")
        password = request.args.get("password")
        does_account_exist = db.user_auth(username, password)
        if (does_account_exist == True):
            flash("Account already exists") #tried registering with taken username (None, None) is not a valid user/pass combo
            return redirect("/register")
        elif (len(username)<6):
            flash("Username too short, must be at least 6 characters") #username too short, None falls under here too
            return redirect("/register")
        else:
            db.user_creat (username, password)
            flash("Successfully registered")
            return redirect ("/")
    return render_template ("register.html") #have a button that redirects to /

@app.route("/profile/<username>", methods = ["POST", "GET"])
@search
def profile(username):
    if ('username' in session):
        username2 = session ['username']
        data = db.get_all_user_data (username)
        return render_template ("profile.html", username2 = username2, data = data, orderid = orderid)
    else:
        return redirect ("/login")


@app.route("/placeorder/<orderid2>", methods = ["POST", "GET"])
@search
def placeorder(orderid2):
    submit = request.args.get("submit")
    if (submit == "Submit"):
        orderid2 = orderid
        username = session ['username']
        store = request.args.get("store")
        food = request.args.get("food")
        cost = request.args.get("cost")
        offer = request.args.get("offer")
        period1 = request.args.get("period1")
        period2 = request.args.get("period2")
        instruction = request.args.get("instruction")
        if (username == "" or store == "" or food == "" or cost == 0 or offer == 0 or period1 == 0 or period2 == 0 or instruction == ""):
            flash("Order incomplete")
            return redirect ("/placeorder/" + str(orderid))
        else:
            db.order_creat(orderid, username, store, food, cost, offer, period1, period2, instruction)
            tmp = orderid2
            orderid = int(orderid) + 1
            username = ""
            store = ""
            food = ""
            cost = 0
            offer = 0
            period1 = 0 
            period2 = 0
            instruction = "" 
            return redirect ("/success/" + str(tmp))
    if ('username' in session):
        username2 = session ['username']
        data = {'username':username2}
        return render_template ("orders.html", username2 = username2, data = data, orderid = orderid2);
    else:
        return render_template ("/login")
           
@app.route("/success/<orderid>")
@search
def success(orderid):
    username = session ['username']
    data = []
    data.append (username)
    return render_template ("success.html", data = data, orderid = orderid)


@app.route("/loadorders/<id2>")
@search
def loadorder(id2):
    data = db.get_all_order_data(id2);
    comment = request.args.get("comment")
    submitc = request.args.get("submitc")
    if (submitc == "Submit" and comment != ""):
        db.add_comment(comment, id2)
        comment = ""
        return redirect ("/loadorders/" + str(id2))
    if ('username' in session):
        username2 = session ['username']
    return render_template ("loadorder.html", username2= username2, data = data, orderid = orderid )

@app.route("/logout")
@search
def logout():
    session.pop('username', None)
    flash('You are logged out')
    return redirect("/")


@app.route("/results", methods=["POST", "GET"])
@search
def results():
    results={};
    try:
        #geo = request.form['geo'];
        #term= request.form['term'];
        geo=False;
        term = "sushi";
    except:
        flash("Please enter a term");
        return render_template("results.html",results=results);
    if(geo):
        lat = request.form["lat"];
        lon = request.form["lon"];
    else:
        try:
            for i in request.form:
                flash(i);
            loc = request.form["loc"];
            loc="brooklyn";
            results = yelp.search(term,loc);
            if(results==None):
                flash("No results came up");
            return jsonify(results);
        except:
            flash("Please enter a location or check automatic");
    flash("fail");
    return render_template("results.html",results=results);


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0')
