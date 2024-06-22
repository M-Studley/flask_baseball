from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateTimeLocalField, DecimalField, EmailField
from wtforms.validators import InputRequired


# Login Form

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


# Registration Form

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired()])
    user_name = StringField('User Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Register')


# Team Form

class TeamForm(FlaskForm):
    team_name = StringField('Team Name', validators=[InputRequired()])
    team_mascot = StringField('Team Mascot', validators=[InputRequired()])
    submit = SubmitField('Submit')


# Practice Form

class PracticeForm(FlaskForm):
    practice_length = DecimalField('Practice Length', validators=[InputRequired()])
    practice_date = DateTimeLocalField('Practice Date', format='%m-%d-%Y', validators=[InputRequired()])
    teams = SelectField('Teams', choices=[])
    submit = SubmitField('Add Practice')
