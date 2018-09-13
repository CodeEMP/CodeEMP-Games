from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context
import jwt
from app import db, login

friends = db.Table('friend',
    db.Column('friender_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('friended_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    friended = db.relationship(
        'User', secondary=friends,
        primaryjoin=(friends.c.friender_id == id),
        secondaryjoin=(friends.c.friended_id == id),
        backref=db.backref('friends', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def check_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def friend(self, user):
        if not self.is_friend(user):
            self.friended.append(user)

    def unfriend(self, user):
        if self.is_friend(user):
            self.friended.remove(user)

    def is_friend(self, user):
        return self.friended.filter(
            friends.c.friended_id == user.id).count() > 0

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
