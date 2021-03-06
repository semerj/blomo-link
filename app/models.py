from app import db, bcrypt
import datetime


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')
    email = db.Column(db.String(120), index=True, unique=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    links = db.relationship('Link', backref='user', lazy='dynamic')

    def __init__(self, username, password, email):
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
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
        return '<user {}>'.format(self.username)


class Link(db.Model):
    __tablename__ = "links"
    id = db.Column(db.Integer, primary_key = True)
    longurl = db.Column(db.Text(), index=False)
    shorturl = db.Column(db.String(140), index=True, unique=True)
    timestamp = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, longurl, shorturl):
        self.longurl = longurl
        self.shorturl = shorturl
        self.timestamp = datetime.datetime.utcnow()

    def __repr__(self):
        return '<long {}, short {}>'.format(self.longurl, self.shorturl)

    def serialize(self):
        return {
            'longurl': self.longurl,
            'shorturl': self.shorturl,
            'timestamp': self.timestamp,
        }

class Click(db.Model):
    __tablename__ = "clicks"
    id = db.Column(db.Integer, primary_key = True)
    shorturl = db.Column(db.String(140), db.ForeignKey('links.shorturl'))
    timestamp = db.Column(db.DateTime())

    def __init__(self, shorturl):
        self.shorturl = shorturl
        self.timestamp = datetime.datetime.utcnow()

    def __repr(self):
        return '<short {}, time {}>'.format(self.shorturl, self.timestamp)
