import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app.database.database import Database

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
password_hashing = Bcrypt(app)
db = Database()
login = LoginManager(app)


from app import routes, models # noqa

if __name__ == '__main__':
    app.run(debug=True)
