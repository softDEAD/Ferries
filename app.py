from flask import Flask,request,url_for,redirect,render_template, flash, session
import json, urllib2
from pymongo import Connection

app=Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

conn = Connection()
db = conn['accountinfo']
users = db.users

@app.route("/")
def index():
    return render_template ("index.html")

@app.route("/login")
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
        i = users.find({'name':username, 'pw':password}).count()
        print i
        does_account_exist = (users.find({'name':username, 'pw':password}).count() == 1)
        if (does_account_exist == True):
            user_list = db.users.find({'name':username, 'pw':password})
            user = user_list[0]
            new_login_count = user['logincount'] + 1
            users.update({'name':username}, {"$set": {'logincount':new_login_count}})
            session ['username'] = username
            session ['logins'] = new_login_count
            return redirect("/welcome")
        flash ("Invalid Username or Password")
        return redirect ("/")
    
    return render_template ("login.html")

@app.route("/register")
def register():
    if (session.get('username') != None):
        flash ("You are already logged in!")
        return redirect ("/")
    register = request.args.get("register")
    if (register == "Register"):
        username = request.args.get("username")
        password = request.args.get("password")
        does_account_exist = (users.find({'name':username}).count() > 0)
        if (does_account_exist == True):
            flash("Account already exists") #tried registering with taken username (None, None) is not a valid user/pass combo
            return redirect("/register")
        elif (len(username)<6):
            flash("Username too short, must be at least 6 characters") #username too short, None falls under here too
            return redirect("/register")
        elif (len(password)<8):
            flash("Password too short, must be at least 8 characters") #password too short, None falls under here too
            return redirect("/register")
        else:
            db.users.insert({'name':username,'pw':password,'logincount':0,'info':""})
            flash("Successfully registered")
            return redirect ("/")
    return render_template ("register.html") #have a button that redirects to /



if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0')
