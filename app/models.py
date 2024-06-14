from app import db, login
from flask_login import UserMixin
from dataclasses import dataclass


# User Model
@dataclass
class User(UserMixin):
    id: int
    user_name: str
    password: str


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
