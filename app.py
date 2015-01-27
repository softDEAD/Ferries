from flask import Flask,request,url_for,redirect,render_template, flash, session
import json, urllib2
from functools import wraps
import db_helper as db
import yelp

app=Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

orderid = db.get_id()
id = 0
orders2 = []

def search(func):
    @wraps(func)
    def inner(*args,**kwargs):
        global orders2
        select = request.args.get("select")
        search = request.args.get("search")
        searchsubmit = request.args.get("searchsubmit")
        if ('username' in session and session.get('username') != None):
            loggedin = True
        else:
            loggedin = False
        if(searchsubmit == "Search" and search != ""):
            if (select == "Period"):
                orders2 = db.get_orders ([], [int(search)])
            elif (select == "Store"):
                orders2 = db.get_orders ([str(search)], [])
            else:
                return redirect("/profile/" + str(search))
        
            return redirect(url_for('index'), orders2 = orders2)
        else:
            return func(*args,**kwargs)
    return inner

@app.route("/", methods = ["POST", "GET"])
@search
def index():
    global orderid
    global orders2
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
        return render_template ("index.html", orders2 = orders2, orderid = orderid, loggedin = loggedin, username2 = username2)



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
        return redirect ("/")
    register = request.args.get("register")
    if (register == "Register"):
        username = request.args.get("username")
        password = request.args.get("password")
        does_account_exist = db.user_exists(username)
        if (does_account_exist):
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
        if (username == username2):
            myprofile = True
        else:
            myprofile = False
        
        submit = request.args.get("frees")
        submit1 = request.args.get("lunch")
        submit2 = request.args.get("repup")
        submit3 = request.args.get("repdown")
        submit4 = request.args.get("submitc")
        submit5 = request.args.get("comment")

        if (submit == "submit"):
            frees = request.args.get("fname")
            db.change_frees(username, frees)
            return redirect("/profile/" + str(username))
        if (submit1 == "submit"):
            lunch = request.args.get("lname")
            db.change_lunch(username, lunch)
            return redirect("/profile/" + str(username))

        if (submit2 == "submit"):
            db.plus_rep(username)
            return redirect("/profile/" + str(username))

        if (submit3 == "submit"):
            db.minus_rep(username)
            return redirect("/profile/" + str(username))

        if (submit4 == "submit" and submit5 != "" ):
            db.profile_comment(username, str(username) + "says: " + submit5)
            return redirect("/profile/" + str(username))
            
        return render_template ("profile.html", myprofile = myprofile, username2 = username2, data = data, orderid = orderid)
    else:
        flash ("You are not logged in")
        return redirect ("/")


@app.route("/placeorder/<orderid2>", methods = ["POST", "GET"])
@search
def placeorder(orderid2):
    if ('username' not in session or session ['username'] == None):
        flash ("You are not logged in")
        return redirect ("/")
    global orderid
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
            db.up_id()
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
    print (data)
    comment = request.args.get("comment")
    submitc = request.args.get("submitc")
    if (submitc == "Submit" and comment != ""):
        db.add_comment(comment, id2)
        comment = ""
        return redirect ("/loadorders/" + str(id2))
    if ('username' in session and session['username'] != data ['username']):
        username2 = session ['username']
        takenby = data ['takenby']
    else:
        takenby= True
    if (takenby == ""):
        taken = request.args.get("Take Order")
        if (taken == "taken"):
            db.take_order(username2, id2)
            return redirect ("/loadorders/" + str(id2))
    elif (takenby == db.get_order_data(id2, 'takenby') and session['username'] == data ['username'] and fulfilled == False):
        fulfillable = True
        fulfilled = False
        ofilled = request.args.get ("Order Has Fulfilled")
        if (ofilled == "fill"):
            orders = db.order_fulfill(id2)
            fulfilled = True
            fulfillable = False
            return render_template ("loadorder.html", fulfillable = fulfillable, fulfilled = fulfilled, takenby = takenby, username2= username2, data = data, orderid = orderid )
    else:
        fulfillable = False
        fulfilled = False
    username2 = session['username']    
    return render_template ("loadorder.html", fulfillable = fulfillable, fulfilled = fulfilled, takenby = takenby, username2 = username2, data = data, orderid = orderid )


@app.route("/logout")
@search
def logout():
    session.pop('username', None)
    loggedin = False
    flash('You are logged out')
    return redirect("/")


@app.route("/results", methods=["POST", "GET"])
@search
def results():
    results={};
<<<<<<< HEAD
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
=======
    error="";
    term="";
    loc="";
    if request.method=='POST':
        geo = 1 == len(request.form.getlist('geo'));
        term= request.form['term'];
        if(term==""):
            flash("Please enter a term.");
            return render_template("results.html",results=results);
        if(geo):
            lat = request.form["lat"];
            lon = request.form["lon"];
            results=yelp.searchbound(term,lat,lon);
        else:
            loc = request.form["loc"];
            if(loc==""):
                flash("Please enter a location or check automatic");
                return render_template("results.html",results=results);
            results = yelp.search(term,loc);
    if(results==None):
        flash("No results came up");
>>>>>>> dionis
    return render_template("results.html",results=results);

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0')
