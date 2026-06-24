from flask import Flask, render_template, request, redirect, url_for
from models import db, Document, URL
from scraper import scrape_url
import Levenshtein

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()

# ======================
# HOME
# ======================
@app.route("/")
def home():
    docs = Document.query.all()

    total_docs = len(docs)
    total_words = sum(len(doc.content.split()) for doc in docs)

    docs_per_year = {}
    for doc in docs:
        year = doc.year
        docs_per_year[year] = docs_per_year.get(year, 0) + 1

    return render_template("home.html",
                           total_docs=total_docs,
                           total_words=total_words,
                           docs_per_year=docs_per_year)

# ======================
# SCRAPPER
# ======================
@app.route("/scrapper")
def scrapper():
    urls = URL.query.all()
    return render_template("scrapper.html", urls=urls)

@app.route("/scrape/<int:url_id>")
def run_scraper(url_id):
    url = URL.query.get(url_id)
    scrape_url(url)
    url.scraped = True
    db.session.commit()
    return redirect(url_for("scrapper"))

# ======================
# CONFIGURATION
# ======================
@app.route("/config", methods=["GET", "POST"])
def config():
    if request.method == "POST":
        new_url = request.form["url"]
        db.session.add(URL(link=new_url))
        db.session.commit()
        return redirect("/config")

    urls = URL.query.all()
    return render_template("config.html", urls=urls)

# ======================
# SEARCH
# ======================
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    results = []

    docs = Document.query.all()

    for doc in docs:
        words = doc.content.split("\n")
        for line in words:
            score = Levenshtein.ratio(query.lower(), line.lower())
            if score > 0.5:
                results.append({
                    "url": doc.url,
                    "text": line,
                    "score": round(score * 100, 3)
                })

    return render_template("search.html", query=query, results=results)

if __name__ == "__main__":
    app.run(debug=True)