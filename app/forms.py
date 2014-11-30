from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class ShortenFrom(Form):
    longurl = StringField('longurl', validators=[DataRequired()])
    shorturl = StringField('short', validators=[DataRequired()])

'''
from flask.ext.wtf import Form, TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from models import db, User


class SignupForm(Form):
    username = TextField("Username", [
        validators.Required("Please enter your username.")
        ])
    email = TextField("Email", [
        validators.Required("Please enter your email address."),
        validators.Email("Please enter your email address.")
        ])
    password = PasswordField('Password', [
        validators.Required("Please enter a password.")
        ])
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True
'''