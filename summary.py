from flask import Flask, render_template, request
import os
import requests
from forms import UrlSearchForm

import nltk
nltk.data.path.append('./nltk_data/')

from newspaper import Article
from wordcloud import WordCloud

import base64
import io
import datetime

def get_wordcloud(text):
    pil_img = WordCloud().generate(text=text).to_image()
    img = io.BytesIO()
    pil_img.save(img, "PNG")
    img.seek(0)
    img_b64 = base64.b64encode(img.getvalue()).decode()
    return img_b64

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def index():
    errors = []
    urlsearch = UrlSearchForm(request.form)

    if request.method == "POST":
        
        try:
            return search_results(urlsearch)
        except:
            errors.append(
                "Unable to get the URL.  Please enter a valid URL for news article."
            )       
    return render_template("index.html", form = urlsearch, errors = errors)

# @app.route("/results", methods = ["GET", "POST"])
def search_results(urlsearch):
    urlsearch = UrlSearchForm(request.form)
    search_string = urlsearch.data['search']

    article = Article(search_string)

    article.download()
    article.parse()
    # nltk.download("punkt")
    article.nlp()

    data = article.text
    title = article.title
    # date = article.publish_date
    # published_date = date.strftime("%d %B %Y")
    # author = article.authors[0]

    # image = article.top_image

    # cloud = get_wordcloud(data)

    # summary = article.summary

    return render_template("results.html", search_string = search_string, title = title)


    # return render_template("results.html", search_string = search_string, data = data, title=title, published_date=published_date, author = author, image = image, cloud = cloud)

    # return render_template("results.html", search_string = search_string, data = data, title=title, published_date=published_date, author = author, image = image, cloud = cloud, summary = summary)           
if __name__ == '__main__':
      app.run()