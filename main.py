import sys
import os.path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, g, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

from test_package import models
from test_package import forms
from test_package import utils

app = Flask(__name__)
app.config.from_object('test_package.config.DevConfig')  # DATABASE = 'main.db'

csrf = CSRFProtect()
csrf.init_app(app)

active_db = app.config['DATABASE']
models.db.init(active_db)
models.initialize_db()

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'To access this page please login in'

@login_manager.user_loader
def load_user(user_id):
    return models.Writer.get_or_none(user_id)

@app.before_request
def before_request():
    g.db = models.db
    g.db.connect(reuse_if_open=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        try:
            website_user = models.Writer.get(models.Writer.email)
        except models.DoesNotExist:
            website_user = models.Writer.create(
                    first_name = form.first_name.data,
                    last_name = form.last_name.data,
                    username = form.username.data,
                    password = bcrypt.generate_password_hash(form.password.data),
                    email = register_form.email.data
                )
            login_user(website_user)
            user_account = website_user.username
            return redirect(url_for('member', member=user_account))
        else:
            flash("An account already exists with the provided email")
            return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/<member>', methods=['POST'])
@login_required
def member(member):
    return render_template('registered.html', name=member)

@app.route('/login')
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            access_user = models.Writer.get(models.Writer.username)
        except models.DoesNotExist:
            flash("No account exists under that user")
            return redirect(url_for('index'))
        valid_password = bcrypt.check_password_hash(
                            access_user.password, 
                            form.password.data
                            )
        if not valid_password:
            flash("The username and/or password are invalid")
            return redirect(url_for('login'))
        login_user(access_user)
        return utils.set_redirect("index")
    return render_template('signup.html', form=form)



    

# # @app.route('/account', methods=['GET', 'POST'])
# # @login_required
# # def account():
    
            



# if __name__ == '__main__':
#     models.alter_schema(active_db)