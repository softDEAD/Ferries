from flask import Flask,request,url_for,redirect,render_template, flash, session
import json, urllib2
from functools import wraps
import db_helper as db
import yelp

app=Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

global orderid
sample = {
    "businesses":
    [
	{
	    "categories": 
            [
		[
		    "Local Flavor",
                    "localflavor"
                ],
		[
		    "Mass Media",
                    "massmedia"
                ]
	    ],
	    "display_phone": "+1-415-908-3801",
            "id": "yelp-san-francisco",
            "is_claimed": True,
            "is_closed": False,
            "image_url": "http://s3-media2.ak.yelpcdn.com/bphoto/7DIHu8a0AHhw-BffrDIxPA/ms.jpg",
            "location": 
            {
		"address": 
                [
		    "140 New Montgomery St"
                ],
		"city": "San Francisco",
                "country_code": "US",
                "cross_streets": "3rd St & Opera Aly",
                "display_address": 
                [
		    "140 New Montgomery St",
                    "(b/t Natoma St & Minna St)",
                    "SOMA",
                    "San Francisco, CA 94105"
                ],
		"neighborhoods": 
                [
		    "SOMA"
                ],
		"postal_code": "94105",
                "state_code": "CA"
            },
	    "mobile_url": "http://m.yelp.com/biz/4kMBvIEWPxWkWKFN__8SxQ",
            "name": "Yelp",
            "phone": "4159083801",
            "rating_img_url": "http://media1.ak.yelpcdn.com/static/201012161694360749/img/ico/stars/stars_3.png",
            "rating_img_url_large": "http://media3.ak.yelpcdn.com/static/201012161053250406/img/ico/stars/stars_large_3.png",
            "rating_img_url_small": "http://media1.ak.yelpcdn.com/static/201012162337205794/img/ico/stars/stars_small_3.png",
            "review_count": 3347,
            "snippet_image_url": "http://s3-media2.ak.yelpcdn.com/photo/LjzacUeK_71tm2zPALcj1Q/ms.jpg",
            "snippet_text": "Sometimes we ask questions without reading an email thoroughly as many of us did for the last event.  In honor of Yelp, the many questions they kindly...",
            "url": "http://www.yelp.com/biz/yelp-san-francisco",
            "menu_provider": "yelp",
            "menu_date_updated": 1317414369
        }
    ],
    "region": 
    {
	"center": 
        {
	    "latitude": 37.786138600000001,
            "longitude": -122.40262130000001
        },
	"span": 
        {
	    "latitude_delta": 0.0,
            "longitude_delta": 0.0
        }
    },
    "total": 10651
}


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
            session ['username'] = username
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
    search = True
    if(search):
        term = request.args.get("term");
        loc = request.args.get("loc");
        results = yelp.search("restaurant","New York");
        if(results==None):
            flash("No results came up")
        return render_template ("results.html",results=results)
    else:
        return render_template("results.html", results=sample)


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0')
