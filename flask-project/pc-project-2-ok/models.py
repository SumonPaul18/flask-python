from extensions import db
from flask_login import UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True)
    email = db.Column(db.String(256), unique=True)
    name = db.Column(db.String(256))
    profile_pic = db.Column(db.String(256))

class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)