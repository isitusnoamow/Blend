from flask import Flask, redirect, url_for, render_template, request
import pymongo
from datetime import datetime, timezone
import math
from pymongo.message import _EMPTY, query
from bson.objectid import ObjectId

from dbtest import addlisting, deactivatelisting, landl, searchlisting
with open('secret.txt') as f:
    secret = f.read()

client = pymongo.MongoClient(f"{secret}")
db = client['borrow']
listers = db['listings']
users = db['users']



app = Flask (__name__)
#setup website

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/lend/", methods = ["POST", "GET"])
def lend():
	if request.method == "POST":
		dist = request.form["dist"]
		item = request.form["obj"]
		return redirect(url_for("borrow_ds", distance=dist, search_entry=item))
	else:
		return render_template("lend.html")

@app.route("/lend/success", methods=["POST"])
def lendsuccess():
	if request.method == "POST":
		user = "person"
		item = request.form["item"]
		price = request.form["price"]
		lendtime = request.form["lendtime"]
		lat = float(request.form["latitude"])
		long = float(request.form["longitude"])
		picture = request.form["image"]
		coordinate = [lat,long]
		addlisting(user,item,price,lendtime,coordinate,picture)
		borrow = False
		return render_template("success.html", borrow=borrow)

@app.route("/login/", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		name = request.form["username"]
		pwd = request.form["password"]
		return redirect(url_for("listings")) #change this later
	else:
		return render_template("login.html")

@app.route("/search/")
def search():
	return render_template("search.html")

@app.route("/searchresult/",methods=["POST","GET"])
def searchresult():
	if request.method == "POST":
		item = request.form["item"]
		distance = float(request.form["distance"])
		lat = float(request.form["latitude"])
		long = float(request.form["longitude"])
		coods = [lat,long]
		queryitems = searchlisting(item,distance,coods)
		return render_template("listolistings.html",queryitems=queryitems)
	else:
		return redirect(url_for('search'))
	

@app.route("/listings/",methods=["POST","GET"])
def listings():
	if request.method == "POST":
		lat = float(request.form["latitude"])
		long = float(request.form["longitude"])
		queryitems = []
		for listing in listers.find({"active": True}):
			if landl(lat,long,listing['location'][0],listing['location'][1],100):
				queryitems.append(listing)
		return render_template("listolistings.html", queryitems=queryitems)
	else:
		return render_template("listings.html")

@app.route("/borrow/success", methods=["POST"])
def borrowsuccess():
	if request.method == "POST":
		obid = request.form['id']
		deactivatelisting("person2", ObjectId(obid))
		borrow = True
		return render_template("success.html", borrow=borrow)

@app.route("/listing/<id>")
def listing(id):
	thing = listers.find_one({"_id": ObjectId(id)})
	active = thing["active"]
	return render_template("listing.html", listing=thing, active=active)

#start website
if __name__ == "__main__":
	app.run(debug=True,host="localhost")