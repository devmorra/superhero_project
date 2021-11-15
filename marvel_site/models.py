from typing import Sequence
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Sequence, func, desc
from flask_migrate import Migrate
import uuid
from datetime import datetime
from sqlalchemy.sql.expression import desc

# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import for Secrets Module (Given by Python)
import secrets

from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
loginManager = LoginManager()
ma = Marshmallow()

@loginManager.user_loader
def loadUser(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    # drone = db.relationship('Drone', backref = 'owner', lazy = True)

    def __init__(self,email,first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self,length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return self

# idSequence = Sequence('hero_id_seq')

class Hero(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    comics_appeared_in = db.Column(db.Integer, nullable=False)
    super_power = db.Column(db.String(150), nullable=True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    owner = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, name, description, comics_appeared_in, super_power, owner_token):
        self.id = self.setID()
        self.name = name
        self.description = description
        self.comics_appeared_in = comics_appeared_in
        self.super_power = super_power
        self.date_created = datetime.utcnow()
        self.owner = owner_token

    def setID(self):
        maxID = db.session.query(func.max(Hero.id)).scalar()
        if maxID is None:
            return 1
        else:
            return int(maxID) + 1

class HeroSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'comics_appeared_in', 'super_power', 'date_created','owner']

hero_schema = HeroSchema()
heroes_schema = HeroSchema(many=True)
