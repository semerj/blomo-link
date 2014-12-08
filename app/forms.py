from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Length, Email, URL, Regexp


class LoginForm(Form):
    username = StringField('Username',
        validators=[DataRequired(message=u'This field is required')])
    password = StringField('Password',
        validators=[DataRequired(message=u'This field is required'),
                    Email(message=u'Please enter a valid email address')])
    remember_me = BooleanField('remember_me', default=False)


class ShortenForm(Form):
    longurl = StringField('Long url', 
        validators=[DataRequired(message=u'This field is required'), 
                    URL(message=u'Please provide a properly formatted URL')])
    shorturl = StringField('Short name',
        validators=[DataRequired(message=u'This field is required'),
                    Regexp(regex=r'[A-Za-z0-9]', 
                           message=u'Please use only alphanumeric characters')])

class RegistrationForm(Form):
    username = StringField('New username',
        validators=[DataRequired(message=u'This field is required'), 
                    Length(min=4, max=20, message=u'Please enter at least 4 characters'),
                    Regexp(regex=r'[A-Za-z0-9]',
                           message=u'Please use only alphanumeric characters')])
    password = StringField('New password',
        validators=[DataRequired(message=u'This field is required'), 
                    Length(min=4, message=u'Please enter at least 4 characters')])
    email = StringField('Email',
        validators=[DataRequired(message=u'This field is required'),
                    Email(message=u'Please enter a valid email address')])
