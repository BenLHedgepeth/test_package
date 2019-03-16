import sys
import os.path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, g, render_template, redirect
from flask_login import LoginManager, login_user
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

from test_package import models
from test_package import forms

app = Flask(__name__)
app.config.from_object('test_package.config.DevConfig')  # DATABASE = 'main.db'

csrf = CSRFProtect()
csrf.init_app(app)

models.db.init(app.config['DATABASE'])
models.initialize_db()

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return models.get_or_none(user_id)

@app.before_request
def before_request():
    g.db = models.db
    g.db.connect(reuse_if_open=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    form = forms.RegisterForm()
    if form.validate_on_submit():

        models.Writer.create(
            username=form.username.data, 
            password=bcrypt.generate_password_hash(form.password.data), 
            email=form.email.data
            )

        return render_template('registered.html')
    return render_template('signup.html', form=form)



# @app.route('/login')
# def login():
#     form = forms.LoginForm()
#     if form.validate_on_submit():
#         try:
#             user = models.get(models.Writer.username == form.username.data)
#         except models.DoesNotExist:
#             flash("The username and/or email is not valid")
#         else:
#             login_user(user)
#             return "Logged in!"
            



if __name__ == '__main__':
    print(app.config['DATABASE'])