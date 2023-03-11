from webApplication import db
from flask_login import UserMixin

class user_accounts(db.Model, UserMixin):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), unique=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password
