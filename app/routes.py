from flask import render_template, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app import app, db
from app.models import User
from app.forms import LoginForm


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    form_username = form.username.data
    form_password = form.password.data
    query = "SELECT * FROM `user` WHERE `user_name` = %s"
    user_data = db.fetchone(query, (form_username,))

    if form.validate_on_submit():
        user = User(**user_data)
        password = user.password

        if not user or password != form_password:
            flash('Invalid username or password!')
            return redirect(url_for('login'))

        login_user(user)
        session.permanent = True
        return redirect(url_for('index'))
    return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
