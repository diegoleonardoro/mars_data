
# Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.

from flask import Flask, render_template
import pymongo

import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars_data
collection = db.data_scraped


# @app.route("/")
# def home():
#   data = mongo.db.collection.find()
#  return render_template("index.html", mars_data=data)


@app.route("/scrape")
def scraper():
    mars_scrapred_data = list(db.collection.find())
    print(mars_scrapred_data)

    return render_template("index.html", data=mars_scrapred_data)


if __name__ == "__main__":
    app.run(debug=True)
