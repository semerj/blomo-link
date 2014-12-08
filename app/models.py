from app import db
import datetime


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')
    #reset_password_token = db.Column(db.String(100), nullable=False, default='')
    email = db.Column(db.String(120), index=True, unique=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    links = db.relationship('Link', backref='user', lazy='dynamic')
    #active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.timestamp = datetime.datetime.utcnow()

    def is_authenticated(self):
        '''Return True if the user is authenticated.'''
        return True

    def is_active(self):
        '''True, as all users are active'''
        return True

    def is_anonymous(self):
        '''False, as anonymous users aren't supported.'''
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<user %r>' % (self.username)


class Link(db.Model):
    __tablename__ = "link"
    id = db.Column(db.Integer, primary_key = True)
    longurl = db.Column(db.String(140), index=True)
    shorturl = db.Column(db.String(140), index=True, unique=True)
    timestamp = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, longurl, shorturl):
        self.longurl = longurl
        self.shorturl = shorturl
        self.timestamp = datetime.datetime.utcnow()

    def __repr__(self):
        return '<long %r, short %r>' % (self.longurl, self.shorturl)

    def serialize(self):
        return {
            'longurl': self.longurl,
            'shorturl': self.shorturl,
            'timestamp': self.timestamp,
        }   

class Click(db.Model):
    __tablename__ = "click"
    id = db.Column(db.Integer, primary_key = True)
    shorturl = db.Column(db.String(140), db.ForeignKey('link.shorturl'))
    timestamp = db.Column(db.DateTime())

    def __init__(self, shorturl):
        self.shorturl = shorturl
        self.timestamp = datetime.datetime.utcnow()

    def __repr(self):
        return '<short %r, time %r>' % (self.shorturl, self.timestamp)

