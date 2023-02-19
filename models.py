from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from server import login_manager

db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(db.Model, UserMixin):
    '''A User'''

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String(255), unique = True, nullable = False)
    first_name = db.Column(db.String(255), nullable = False)
    last_name = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(255), unique = True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = False)

    def __init__(self, username, first_name, last_name, email, password):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = generate_password_hash(password)
    
    def __repr__(self):
        return f"<User user_id={self.user_id} username={self.username}>"

    @classmethod
    def create_user(cls, username, first_name, last_name, email, password):
        '''Create and return a new user'''

        return cls(username = username, first_name = first_name, last_name = last_name, email = email, password = password)

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter(User.email == email).first()




def connect_to_db(flask_app, db_uri="postgresql:///portfoliocraft", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app
    connect_to_db(app)