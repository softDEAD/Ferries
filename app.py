from flask import Flask,request,url_for,redirect,render_template, flash
import json, urllib2

app=Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route("/")
def index():
    return render_template ("index.html")

@app.route("/login")
def login():
    return render_template ("index.html");

@app.route("/register")
def register():
    return render_template ("index.html");



