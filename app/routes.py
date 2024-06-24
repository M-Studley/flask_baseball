from flask import render_template, redirect, url_for, flash, session, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import generate_password_hash, check_password_hash
from app import app, db, login
from app.models import User, Team, Practice
from app.forms import LoginForm, RegistrationForm, TeamForm, PracticeForm


# HOME PAGE

@app.route('/')
def index():
    return render_template('index.html')


# USER REGISTRATION

@app.route('/register', methods=['GET', 'POST'])
def user_registration():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            form_first_name = form.first_name.data
            form_last_name = form.last_name.data
            form_email = form.email.data
            form_user_name = form.user_name.data
            form_password = generate_password_hash(form.password.data)

            user = User(first_name=form_first_name,
                        last_name=form_last_name,
                        email=form_email,
                        user_name=form_user_name,
                        password=form_password)
            db.execute("""
            INSERT INTO `user` 
            (`first_name`, `last_name`, `email`, `user_name`, `password`) 
            VALUES (%s, %s, %s, %s, %s)
            """, (user.first_name, user.last_name, user.email, user.user_name, user.password))

            flash('Registration Successful!', category='success')
            return redirect(url_for('user_login', first_name=user.first_name))

        flash('Please fill out all fields...', category='warning')

    return render_template('register.html', title='Register', form=form)


# USER - LOGIN, LOGOUT

@app.route('/login', methods=['GET', 'POST'])
def user_login():
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
        print(password)
        if not user:
            if not check_password_hash(password, form_password):
                flash('Invalid username or password!', category='danger')
                return redirect(url_for('user_login'))

        login_user(user)
        session.permanent = False
        session['first_name'] = user.first_name
        flash('Log in success!', category='success')
        return redirect(url_for('index'))

    return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login.unauthorized_handler
def unauthorized():
    return redirect(url_for('user_login'))


# TEAM - MAIN, UPDATE, DELETE

@login_required
@app.route('/teams', methods=['GET', 'POST'])
def teams():
    form = TeamForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            team_name = request.form.get('team_name')
            team_mascot = request.form.get('team_mascot')
            team = Team(team_name=team_name, team_mascot=team_mascot)
            db.execute('INSERT INTO `team` (`team_name`, `team_mascot`) VALUES (%s, %s)',
                       (team.team_name, team.team_mascot))
            flash('Team successfully created!', category='success')
            return redirect(url_for('teams'))

        flash('Please fill out all fields...', category='warning')

    all_teams = db.fetchall('SELECT * FROM `team`')
    return render_template('teams.html', form=form, teams=all_teams)


@login_required
@app.route('/team_update/<team_id>', methods=['GET', 'POST'])
def team_update(team_id):
    query = "SELECT * FROM `team` WHERE id = %s"
    fetched_team = db.fetchone(query, team_id)
    team = Team(**fetched_team)
    team.team_name = request.form.get('team_name')
    team.team_mascot = request.form.get('team_mascot')
    db.execute('UPDATE `baseball`.`team` SET `team_name` = %s, `team_mascot` = %s WHERE `id`= %s;',
               (team.team_name, team.team_mascot, team.id))
    flash(f'{team.team_name} has been successfully updated!', category='success')
    return redirect(url_for('teams'))


@login_required
@app.route('/team_delete/<team_id>', methods=['GET', 'POST'])
def team_delete(team_id):
    db.execute('DELETE FROM `baseball`.`team` WHERE id = %s', (team_id,))
    flash('Team has been permanently deleted', category='danger')
    return redirect(url_for('teams'))


# PRACTICES - MAIN, UPDATE, DELETE

@login_required
@app.route('/practices', methods=['GET', 'POST'])
def practices():
    form = PracticeForm()
    all_teams = db.fetchall('SELECT * FROM `team`')
    form.teams.choices = [(team['id'], team['team_name']) for team in all_teams]

    if request.method == 'POST':
        if form.validate_on_submit():
            practice_date = request.form.get('practice_date')
            practice_length = request.form.get('practice_length')
            team_id = request.form.get('teams')
            practice = Practice(practice_date=practice_date, practice_length=float(practice_length),
                                team_id=int(team_id))
            db.execute(query="""
            INSERT INTO `practice` 
            (`practice_date`, `practice_length`, `team_id`) 
            VALUES (%s, %s, %s)
            """, data=(practice.practice_date, practice.practice_length, practice.team_id))

            flash('Practice successfully created!', category='success')
            return redirect(url_for('practices'))

        flash('Please fill out all fields...', category='warning')

    all_practices = db.fetchall(
        """
        SELECT 
        `t`.`id`, `t`.`team_name`, `t`.`team_mascot`, 
        `p`.`id` AS `practice_id`, `p`.`practice_date`, `p`.`practice_length`, `p`.`team_id` 
        FROM `team` AS `t` 
        JOIN `practice` AS `p` 
        ON `t`.`id` = `p`.`team_id`
        """
    )
    return render_template('practices.html', form=form, teams=all_teams, all_practices=all_practices)


@login_required
@app.route('/practice_update/<practice_id>', methods=['GET', 'POST'])
def practice_update(practice_id):
    query = "SELECT * FROM `practice` WHERE id = %s"
    fetched_practice = db.fetchone(query, practice_id)
    practice = Practice(**fetched_practice)
    practice.practice_date = request.form.get('practice_date')
    practice.practice_length = request.form.get('practice_length')
    db.execute('UPDATE `baseball`.`practice` SET `practice_date` = %s, `practice_length` = %s WHERE `id`= %s;',
               (practice.practice_date, practice.practice_length, practice.id))
    flash(f'The practice has been successfully updated!', category='success')
    return redirect(url_for('practices'))


@login_required
@app.route('/practice_delete/<practice_id>', methods=['GET', 'POST'])
def practice_delete(practice_id):
    db.execute('DELETE FROM `baseball`.`practice` WHERE id = %s', (practice_id,))
    flash('Practice has been permanently deleted', category='danger')
    return redirect(url_for('practices'))
