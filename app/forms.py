from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Length, Email, URL


class LoginForm(Form):
    username = StringField('Username',
        validators=[DataRequired(message=u'This field is required')])
    password = StringField('Password',
        validators=[DataRequired(message=u'This field is required')])
    remember_me = BooleanField('remember_me', default=False)


class ShortenForm(Form):
    longurl = StringField('Long url', 
        validators=[DataRequired(message=u'This field is required'), 
                    URL(message=u'Please provide a properly formatted URL')])
    shorturl = StringField('Short name',
        validators=[DataRequired(message=u'This field is required')])


class RegistrationForm(Form):
    username = StringField('New username',
        validators=[DataRequired(message=u'This field is required'), 
                    Length(min=4, max=20, message=u'Please enter password at least 4 characters long')])
    password = StringField('New password',
        validators=[DataRequired(message=u'This field is required'), 
                    Length(min=4, message=u'Please enter password at least 4 characters long')])
    email = StringField('Email',
        validators=[DataRequired(message=u'This field is required')])

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