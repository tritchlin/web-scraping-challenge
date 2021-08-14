from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/planet"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    if mars == None:
        return render_template("empty.html")
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scraper():
    # mars api caling mars collection inside planet db
    mars_db = mongo.db.mars
    mars_data = {}
    mars_data['news'] = scrape_mars.scrape_news()
    mars_data['image'] = scrape_mars.scrape_image()
    mars_data['facts'] = scrape_mars.scrape_facts()
    mars_data['hemis'] = scrape_mars.scrape_hemis()
    mars_db.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
