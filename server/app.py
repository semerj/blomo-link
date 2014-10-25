#!/usr/bin/env python

import shelve
from subprocess import check_output
import flask
from flask import request
from os import environ
import string
import random

app = flask.Flask(__name__)
app.debug = True


db = shelve.open("shorten.db")


def create_short_url(long_url):
    new_url = ''.join(random.sample(string.letters, 5))
    base_url = 'http://people.ischool.berkeley.edu/~jsemer/'
    return base_url + new_url + '.html'

def return_html(variable):
    return '''
<html>
  <head>
    <title>bitly-clone</title>
  </head>
  <body>
    <p>Here is your link: ''' + variable + '''</p>
  </body>
</html>
'''

@app.route('/')
@app.route('/home', methods=['GET'])
def home():
    """Builds a template based on a GET request, with some default
    arguements"""
    return flask.render_template('home.html')


@app.route('/shorts', methods=['POST'])
def shorts():
    long_url = request.form['long-url']     # form id from html
    if long_url in db:
        #return return_html(db[long_url])
        return 'url in db'
        #print db.values
        #return db[long_url]
    else:
        db[long_url] = create_short_url(long_url)
        #return return_html(db[request.form['long-url']])
        return_html "url not in db"
        #print db.values
        #return db[request.form['long-url']]
    #print db.values


###
# Wiki Resource:
# GET method will redirect to the resource stored by PUT, by default: Wikipedia.org
# POST/PUT method will update the redirect destination
###
@app.route('/wiki', methods=['GET'])
def wiki_get():
    """Redirects to wikipedia."""
    destination = db.get('wiki', 'http://en.wikipedia.org')
    app.logger.debug("Redirecting to " + destination)
    return flask.redirect(destination)

@app.route("/wiki", methods=['PUT', 'POST'])
def wiki_put():
    """Set or update the URL to which this resource redirects to. Uses the
    `url` key to set the redirect destination."""
    wikipedia = request.form.get('url', 'http://en.wikipedia.org')
    db['wiki'] = wikipedia
    return "Stored wiki => " + wikipedia

###
# i253 Resource:
# Information on the i253 class. Can be parameterized with `relationship`,
# `name`, and `adjective` information
#
# TODO: The representation for this resource is broken. Fix it!
# Set the correct MIME type to be able to view the image in your browser
##/
@app.route('/i253')
def i253():
    """Returns a PNG image of madlibs text"""
    relationship = request.args.get("relationship", "friend")
    name = request.args.get("name", "Jim")
    adjective = request.args.get("adjective", "fun")

    resp = flask.make_response(
            check_output(['convert', '-size', '600x400', 'xc:transparent',
                '-frame', '10x30',
                '-font', '/usr/share/fonts/liberation/LiberationSerif-BoldItalic.ttf',
                '-fill', 'black',
                '-pointsize', '32',
                '-draw',
                  "text 30,60 'My %s %s said i253 was %s'" % (relationship, name, adjective),
                '-raise', '30',
                'png:-']), 200);
    # Comment in to set header below
    # resp.headers['Content-Type'] = '...'

    return resp


if __name__ == "__main__":
    app.run()
    #app.run(port=int(environ['FLASK_PORT']))
