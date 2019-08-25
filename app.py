# Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import urllib3
from urllib3.util.retry import Retry

# Create Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/scrape_mars_db")

# This route queries the Mongo database and passes the mars_data into an html template
@app.route("/")
def index():
    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()

    # Return the template with data
    return render_template("index.html", mars=mars_data)

# Create "/scrape" route to import the srape_mars.py script
@app.route("/scrape")
def scrape():
    # Use the scrape function
    mars_dictionary = scrape_mars.scrape()

    # Update the mongo database
    mongo.db.collection.update({}, mars_dictionary, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)