# auth/views.py renders and manages responses from the login and revister pages.

# flask
from flask import render_template, redirect, request, url_for, flash, current_app
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
# other
from sqlalchemy import or_
# local
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm

# function that checks a username/ email and password (against the hashed
#  password stored in the database)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        user = User.query.filter((User.username==form.username.data) | (User.email==form.username.data)).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)

# log a user out
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

# register a new user. 
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # create new user
        user = User(email=form.email.data,
                    username=form.username.data,
                    full_name=form.full_name.data,
                    password=form.password.data)
        db.session.add(user)
        #flash('You can now login.')
        return redirect(url_for('main.review'))
    return render_template('auth/register.html', form=form)
