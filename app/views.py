from flask import render_template, flash, redirect, session, url_for, request, g, abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from forms import LoginForm, RegistrationForm, ShortenForm
from models import User, Link


linkurl = 'http://localhost:5000/s/'


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    form = ShortenForm()
    return render_template('index.html', form=form)


@login_manager.user_loader
def load_user(id):
    '''loads a user from the database'''
    return User.query.get(int(id))


@app.route("/registration", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('registration.html', form=form)

    elif request.method == 'POST':
        form_is_valid = form.validate_on_submit()
        
        if form_is_valid:
            user = User(request.form['username'], 
                        request.form['password'],
                        request.form['email'])
            db.session.add(user)
            db.session.commit()
            flash('User successfully registered')
            return redirect(url_for('login'))

        else:
            flash('Registration form is not complete')
            return render_template('registration.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'GET': 
        return render_template("login.html", form=form)
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        remember_me = False
        if 'remember_me' in request.form:
            remember_me = True
        
        registered_user = User.query.filter_by(username=username, password=password).first()
        if registered_user is None:
            flash('Username or Password is invalid' , 'error')
            return redirect(url_for('login'))
        
        login_user(registered_user, remember=remember_me)
        flash('Logged in successfully')
        return redirect(request.args.get('next') or url_for('index'))
        #user_is_logged_in = (g.user is not None and g.user.is_authenticated())
        #form_is_valid = form.validate_on_submit()
        #if user_is_logged_in:
        #    return redirect(url_for('index'))
        #if form_is_valid:
        #    return render_template("index.html", form=form)
            #login_user(user)
            #flash("Logged in successfully.")
            #return redirect(request.args.get("next") or url_for("index"))
        #else:
        #    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/s/')
@app.route('/s', methods=['POST', 'GET'])
def shorts():
    form = ShortenForm()
    if request.method == 'POST':
        link = Link(request.form['longurl'], request.form['shorturl'])
        
        user_is_logged_in = (g.user is not None and g.user.is_authenticated())
        form_is_valid = form.validate_on_submit()

        if user_is_logged_in and form_is_valid:
            link.user = g.user
            db.session.add(link)
            db.session.commit()
            flash('Link successfully registered')
            return render_template('shorts.html', shorturl=linkurl + link.shorturl)
        
        elif not user_is_logged_in and form_is_valid:
            db.session.add(link)
            db.session.commit()
            flash('Link successfully registered')
            return render_template('shorts.html', shorturl=linkurl + link.shorturl)
        
        elif not form_is_valid:
            flash('Please validate your url(s)')
            return redirect(url_for('index'))

        else:
            return redirect(url_for('index'))

    elif request.method == 'GET':
        return render_template('index.html', form=form)


@app.route('/s/<url>', methods=['GET'])
def shorts_redirect(url):
    if request.method == 'GET':
        shorturl = Link.query.filter_by(shorturl=url).first()
        if shorturl == None:
            flash('Link not found') #return abort(404)
            return redirect(url_for('index'))

        return redirect(shorturl.longurl)


@app.route('/user')
def user():
    return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def profile(username):
    #user = User.query.filter_by(username=username).first()
    user = User.query.filter_by(id=g.user.id).first()
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
