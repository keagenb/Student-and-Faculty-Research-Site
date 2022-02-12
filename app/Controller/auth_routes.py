from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from flask_sqlalchemy import sqlalchemy
from config import Config
from flask_login import current_user, login_user, logout_user, login_required

from app import db

from app.Controller.auth_forms import RegistrationForm, LoginForm
from app.Model.models import User

bp_auth = Blueprint('auth', __name__)
bp_auth.template_folder = Config.TEMPLATE_FOLDER 

@bp_auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))  

    rform = RegistrationForm()
    if rform.validate_on_submit():
        if rform.student.data == True:
            if rform.faculty.data == True:
                flash('Please select student OR faculty.')
                return redirect(url_for('auth.register'))


        user = User(username=rform.username.data, email=rform.email.data)
        user.set_password(rform.password.data)
        if rform.student.data == True:
            user.usertype = 'student'
        if rform.faculty.data == True:
            user.usertype = 'faculty'
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful.')

        #log in the user to avoid having to login immediately after registering
        login_user(user)

        if rform.student.data==True:
            return redirect(url_for('routes.setup'))
        else: 
            return redirect(url_for('routes.home'))   
    return render_template('register.html', form=rform)

@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))

    loginform=LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(username=loginform.username.data).first()
        if (user is None) or (user.get_password(loginform.password.data)==False):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember = loginform.remember_me.data)
        return redirect(url_for('routes.home'))
    return render_template('login.html', form = loginform)

@bp_auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))