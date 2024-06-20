from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateTimeLocalField, DecimalField
from wtforms.validators import DataRequired, InputRequired


# Login Form

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


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
