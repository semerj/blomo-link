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


@app.route('/', methods=['GET'])
def home():
    return flask.render_template('home.html')


@app.route('/shorts', methods=['POST'])
def shorts():
    long_url = request.form['long-url']
    short = request.form['short-url']
    if long_url in db:
        return flask.render_template('new_url.html', new_url=db[long_url])
    else:
        db[short] = long_url
        return flask.render_template('new_url.html', new_url=short)


@app.route('/shorts/<url>', methods=['GET'])
def shorts_redirect(url):
    return flask.redirect(db[url])


if __name__ == "__main__":
    #app.run()
    app.run(port=int(environ['FLASK_PORT']))
