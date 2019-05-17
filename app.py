# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# create mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# client = pymongo.MongoClient()
# db = client.mars_db
# collection = db.mars_data_entries

@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return  render_template('index.html', mars_data=mars_data)

@app.route("/scrape")
def scraper():
    #db.mars_collection.remove({})
    mars_data = mongo.db.mars_data
    mars = scrape_mars.scrape()
    mars_data.update({}, mars, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)