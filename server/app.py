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


@app.route('/shorts', methods=['POST'])
def shorts():
    long_url = request.form['long-url'].encode('utf-8')
    short = request.form['short-url'].encode('utf-8')
    if long_url in db:
        return flask.render_template('new_url.html', new_url=db[long_url])
    else:
        if short:
            db[short] = long_url
        else:
            short = randomize()
            db[short] = long_url
        return flask.render_template('new_url.html', new_url=short)


@app.route('/shorts/<url>', methods=['GET'])
def shorts_redirect(url):
    url = url.encode('utf-8')
    return flask.redirect(db[url])


if __name__ == "__main__":
    #app.run()
    app.run(port=int(environ['FLASK_PORT']))
