from app import db, login
from flask_login import UserMixin
from dataclasses import dataclass


@login.user_loader
def load_user(user_id):
    query = "SELECT * FROM `user` WHERE `id` = %s"
    data = user_id
    user_data = db.fetchone(query, data)
    if user_data:
        user = User(**user_data)
        return user.id
    return None


# User Model
@dataclass
class User(UserMixin):
    first_name: str
    last_name: str
    email: str
    user_name: str
    password: str
    id: int = None


# Team Model
@dataclass
class Team:
    team_name: str
    team_mascot: str
    id: int = None


# Practice Model
@dataclass
class Practice:
    practice_length: float
    practice_date: str
    team_id: int
    id: int = None
