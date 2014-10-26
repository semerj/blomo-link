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
    """Builds a template based on a GET request, with some default
    arguements"""
    return flask.render_template('home.html')

@app.route('/server/shorts', methods=['POST'])
def shorts():
    long_url = request.form['long-url']
    short_url = request.form['short-url']
    if long_url in db:
        return flask.render_template('new_url.html', new_url=db[long_url])
    else:
        db[long_url] = short_url
        return flask.render_template('new_url.html', new_url=db[long_url])

if __name__ == "__main__":
    app.run()
    #app.run(port=int(environ['FLASK_PORT']))
