from app import db, login
from flask_login import UserMixin
from dataclasses import dataclass


@login.user_loader
def load_user(user_id):
    query = "SELECT * FROM `user` WHERE `id` = %s"
    data = user_id
    user_data = db.fetchone(query, data)
    if user_data:
        return User.id
    return None


# User Model
@dataclass
class User(UserMixin):
    id: int
    user_name: str
    password: str

    @classmethod
    def get_id(cls):
        return cls.id


# Team Model
@dataclass
class Team:
    id: int
    team_name: str
    team_mascot: str


# Practice Model
@dataclass
class Practice:
    id: int
    practice_length: int
    practice_date: str
    team_id: int
