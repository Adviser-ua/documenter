# coding: utf-8
# Konstantyn Davidenko

from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, request, redirect, url_for
from auth.forms import LoginForm, RegistrationForm
from models import User
from flask import Blueprint

auth_bp = Blueprint('auth', __name__, template_folder='templates')


@auth_bp.route('register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('documents.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        form.apply()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


@auth_bp.route('login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('documents.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next = request.args.get('next')
        if next:
            return redirect(next)
        return redirect(url_for('documents.index'))
    return render_template('auth/login.html', title='Sign In', form=form)


@auth_bp.route('logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('documents.index'))
