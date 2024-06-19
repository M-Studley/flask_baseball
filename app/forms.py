from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
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
