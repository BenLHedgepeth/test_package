from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

from wtforms.validators import DataRequired, ValidationError, EqualTo, Email

from test_package import models

class RegisterForm(FlaskForm):
    username = StringField(
            label='Username',
            validators=[
                DataRequired(message="Need Username"),
            ]
        )
    password = PasswordField(
            label="Password",
            validators=[DataRequired(message="Already exists"), 
                        EqualTo('verify', 'Verify Password')
                        ]           
        )
    verify = PasswordField(
            label='Verify',
            validators = [DataRequired()]
        )
    email = StringField (
            label="Email",
            validators=[Email()]
        )

class LoginForm(FlaskForm):
    username = StringField(
            label='Username',
            validators=[
                DataRequired(message="Need Username"),
                # search_user
            ]
        )
    password = PasswordField(
            label="Password",
            validators=[DataRequired(message="Already exists"), 
                        EqualTo('verify', 'Verify Password')
                        ]           
        )
    verify = PasswordField(
            label='Verify',
            validators = [DataRequired()]
        )