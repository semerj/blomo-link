#!/usr/bin/env python

import shelve
from subprocess import check_output
import flask
from flask import request, url_for
from os import environ
import string
import random

app = flask.Flask(__name__)
app.debug = True
db = shelve.open("shorten.db")


def randomize():
    url = ''.join(random.sample(string.letters, 5))
    return url


@app.route('/', methods=['GET'])
def home():
    return flask.render_template('home.html')

# def check_1(short, long_url):
#     if short in db and db[short] != long_url:
#         return flask.render_template('home.html', taken_url="Short url taken. Please try again.")
#     if db[short] = long_url:
#         return flask.render_template('home.html', new_url = short) 

# def check_2():
#     long_url = request.form['long-url'].encode('utf-8')
#     short = request.form['short-url'].encode('utf-8')
#     check_1(short, long_url)
#     if db.key(long_url) != None and db.key(long_url) != short:
#         flask.render_template('home.html', taken_url="The URL already has been shortened before with the value", short, ", do you want to keep it or create a new one?") 
#         answer = raw_input("y/n"+"\n")
#         if answer = "y":
#             flask.render_template('home.html')




@app.route('/shorts', methods=['POST'])
def shorts():
    long_url = request.form['long-url'].encode('utf-8')
    short = request.form['short-url'].encode('utf-8')

    if short in db and db[short] != long_url:
        return flask.render_template('home.html', taken_url="Short url taken. Please try again.")
    elif db[short] = long_url:
        return flask.render_template('home.html', new_url = short) 
    # my syntax is probably wrong...
    elif db.key(long_url) != None and db.key(long_url) != short:
        flask.render_template('home.html', taken_url="The URL already has been shortened before with the value", short, ", do you want to keep it or create a new one?") 
        answer = raw_input("y/n"+"\n")
        if answer = "y":
            make the new url
        if answer = "n":
            tell user the old url
        
    else:
        if short:
            db[short] = long_url
        else:
            short = randomize()
            db[short] = long_url
        return flask.render_template('home.html', new_url=short)


@app.route('/shorts/<url>', methods=['GET'])
def shorts_redirect(url):
    if url.encode('utf-8') in db:
        url = url.encode('utf-8')
        return flask.redirect(db[url])
    else:
        return flask.render_template('404.html'), 404


if __name__ == "__main__":
    #app.run()
    app.run(port=int(environ['FLASK_PORT']))
