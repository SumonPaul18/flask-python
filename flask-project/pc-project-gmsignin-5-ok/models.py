from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(256), unique=True)
     email = db.Column(db.String(256), unique=True)
     password = db.Column(db.String(256))
     confirmed = db.Column(db.Boolean, default=False)

class OAuth(OAuthConsumerMixin, db.Model):
     provider_user_id = db.Column(db.String(256), unique=True)
     user_id = db.Column(db.Integer, db.ForeignKey(User.id))
     user = db.relationship(User)
