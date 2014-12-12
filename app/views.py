from flask import render_template, flash, redirect, \
    session, url_for, request, g, abort, jsonify
from flask.ext.login import login_user, logout_user, \
    current_user, login_required
from app import app, db, login_manager
from forms import LoginForm, RegistrationForm, ShortenForm
from models import User, Link, Click, bcrypt
from sqlalchemy import func
from datetime import datetime, timedelta


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    form = ShortenForm()
    return render_template('index.html', form=form)


@app.route("/registration", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)

    if request.method == 'POST':
        form_is_valid = form.validate_on_submit()

        if form_is_valid:
            username = request.form['username']
            username_exist = User.query.\
                filter_by(username=username).first()

            if username_exist is not None:
                flash("Username already in use. Please try again.")
                return render_template('registration.html', form=form)

            else:
                user = User(form.username.data,
                            form.password.data,
                            form.email.data)
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash('Thanks for signing up! Now create your first blomoLink~')
                return redirect(url_for('index'))

        else:
            flash('Signup form is not complete')
            return render_template('registration.html', form=form)

    elif request.method == 'GET':
        return render_template('registration.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)

    if request.method == 'GET':
        return render_template("login.html", form=form)

    elif request.method == 'POST':
        form_is_valid = form.validate_on_submit()

        if form_is_valid:
            username = form.username.data
            password = form.password.data
            registered_user = User.query.\
                filter_by(username=username).first()

            remember_me = False
            if 'remember_me' in request.form:
                remember_me = True

            if registered_user is not None and \
                bcrypt.check_password_hash(
                    registered_user.password, password):
                login_user(registered_user, remember=remember_me)
                flash('Login successful')
                return redirect(request.args.get('next') or url_for('index'))

            else:
                flash('Username or password is invalid', 'error')
                return render_template('login.html', form=form)

        else:
            return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('index'))


@app.route('/s/')
@app.route('/s', methods=['POST', 'GET'])
def shorts():
    form = ShortenForm(request.form)

    if request.method == 'POST':
        longurl = form.longurl.data
        shorturl = form.shorturl.data
        form_is_valid = form.validate_on_submit()
        user_is_logged_in = (
            g.user is not None and g.user.is_authenticated())

        if form_is_valid:
            shorturl_query = Link.query.\
                filter_by(shorturl=shorturl).first()

            if shorturl_query is not None:
                flash('Link already exists. Try choosing another one.')
                return redirect(url_for('index'))

            else:
                link = Link(longurl, shorturl)

                if user_is_logged_in:
                    link.user = g.user

                db.session.add(link)
                db.session.commit()
                return render_template(
                    'shorts.html',
                    shorturl='{}s/{}'.format(request.url_root, link.shorturl),
                    longurl=link.longurl,
                    user=g.user)

        elif not form_is_valid:
            return render_template('index.html', form=form)

    elif request.method == 'GET':
        return redirect(url_for('index'))


@app.route('/s/<url>', methods=['GET'])
def shorts_redirect(url):
    if request.method == 'GET':
        url_query = Link.query.filter_by(shorturl=url).first()

        if url_query is None:
            return abort(404)
            #will need to take out this flash one 404 page is in place.
            #flash('Link not found')
            #return redirect(url_for('index'))

        else:
            click = Click(url_query.shorturl)
            db.session.add(click)
            db.session.commit()
            return redirect(url_query.longurl)


@app.route('/user')
def user():
    return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))

    else:
        links = Link.query.join(User, (User.id == Link.user_id)).\
            filter(User.username == user.username).\
            order_by(Link.timestamp.desc())

        daysAgo = []
        for x in xrange(8):
            daysAgo.append(
                datetime.date(datetime.utcnow() - timedelta(days=x)))

        # A list of the user's short URLs and long URLs
        listOfLinksQuery = Link.query.\
            join(User, (User.id == Link.user_id)).\
            filter(User.username == user.username).\
            order_by(Link.timestamp.desc())

        listOfKeysShortURL = [c.shorturl for c in listOfLinksQuery]
        listOfLongURL = [c.longurl for c in listOfLinksQuery]

        totalClicksPerLink = []
        for i in xrange(0, len(listOfKeysShortURL)):
            totalClicksPerLink.append(
                int(Click.query.filter(
                    Click.shorturl == listOfKeysShortURL[i]).count()))

        # A list of total clicks for each short URL
        # Broken down by each day of the week, starting with the most recent
        weeklyCounts = [[] for x in xrange(len(listOfKeysShortURL))]
        for key, value in enumerate(listOfKeysShortURL):
            for j in xrange(8):
                weeklyCounts[key].append(
                    int(Click.query.
                        filter(Click.shorturl == value).
                        filter(func.date(Click.timestamp) == daysAgo[j]).
                        count()))

        listOfFullShortURL = [str(request.url_root + 's/' + x)
                          for x in listOfKeysShortURL]
        listOfTimestamps = [datetime.date(link.timestamp) for link in links]

        masterList = zip(listOfLongURL,
                         listOfFullShortURL,
                         listOfKeysShortURL,
                         totalClicksPerLink,
                         weeklyCounts,
                         listOfTimestamps)

        return render_template("user.html",
                               title='Home',
                               user=g.user,
                               links=masterList)
