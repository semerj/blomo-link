from flask.ext.wtf import Form
#from flask.ext.wtf import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class ShortenForm(Form):
    longurl = StringField('longurl', validators=[DataRequired()])
    shorturl = StringField('shorturl', validators=[DataRequired()])


class RegistrationForm(Form):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

'''
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