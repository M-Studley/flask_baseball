from flask import Flask
from database.database import Database
from flask_login import LoginManager

app = Flask(__name__)
db = Database()
login = LoginManager(app)

from app import routes, models  # noqa

if __name__ == '__main__':
    app.run(debug=True)
