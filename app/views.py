from flask import render_template, flash, redirect, session, url_for, request, g, abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from forms import LoginForm
from models import User, Link

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@login_manager.user_loader
def load_user(id):
    '''loads a user from the database'''
    return User.query.get(int(id))

@app.route("/login", methods=["GET", "POST"])
def login():
    '''
    If g.user is set to an authenticated user, then we
    redirect to the index page. The 'g' global is setup by
    Flask as a place to store and share data during the life
    of the request
    '''
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        login_user(user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    return 'Insert registration code here'

@app.before_request
def before_request():
    '''
    login view function checks if g.user is already logged in.
    run before the view function each time a request is received.
    '''
    g.user = current_user

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/shorts', methods=['GET','POST'])
def shorts():
    long_url = request.form['long-url'].encode('utf-8')
    short = request.form['short-url'].encode('utf-8')
    if short in db:
        return flask.render_template('home.html', taken_url="Short url taken. Please try again.")
    else:
        if short:
            db[short] = long_url
        else:
            short = randomize()
            db[short] = long_url
        return flask.render_template('home.html', new_url=short)

@app.route('/shorts/<url>', methods=['GET'])
def shorts_redirect(url):
    shorturl = Link.query.filter_by(shorturl=url).first()
    if shorturl == None:
        flash('Link not found') #return abort(404)
        return redirect(url_for('index'))

    return redirect(shorturl.longurl)
    #return render_template('shorts.html', shorturl='http://localhost:5000/shorts/'+ shorturl.shorturl)

@app.route('/user/<username>')
#@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    #user = g.user
    if user == None:
        flash('User %s not found.' % username)
        return redirect(url_for('index'))

    links = Link.query.join(User, (User.id == Link.user_id)).\
        filter(User.username == user.username).\
        order_by(Link.timestamp.desc())

    return render_template("user.html",
                           title='Home',
                           user=user,
                           links=links)