import sys
import os
from flask import Flask, flash, redirect, url_for
from sqlalchemy.orm.exc import NoResultFound
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.consumer import oauth_authorized, oauth_error
from dotenv import load_dotenv
from extensions import db, login_manager
from models import User, OAuth
from flask_login import current_user, login_user  # Import current_user and login_user here

# Load environment variables from .env file
load_dotenv()

os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# setup Flask application
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersekrit")

# setup database models
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///glu.db"
db.init_app(app)

# setup login manager
login_manager.login_view = 'google.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# setup Google OAuth
blueprint = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=["profile", "email"],
    redirect_to="routes.index"
)
blueprint.backend = SQLAlchemyStorage(OAuth, db.session, user=current_user)
app.register_blueprint(blueprint, url_prefix="/login")

# Import and register the routes blueprint
from routes import routes
app.register_blueprint(routes)

# create/login local user on successful OAuth login
@oauth_authorized.connect_via(blueprint)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with Google.", category="error")
        return False

    resp = blueprint.session.get("/oauth2/v2/userinfo")
    if not resp.ok:
        flash("Failed to fetch user info from Google.", category="error")
        return False

    google_info = resp.json()
    if not google_info:
        flash("No user info returned from Google.", category="error")
        return False

    google_user_id = google_info.get("id")
    if not google_user_id:
        flash("No user ID returned from Google.", category="error")
        return False

    query = OAuth.query.filter_by(
        provider=blueprint.name,
        provider_user_id=google_user_id,
    )
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=google_user_id,
            token=token,
        )

    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in with Google.")
    else:
        user = User(
            email=google_info.get("email"),
            name=google_info.get("name"),
            profile_pic=google_info.get("picture")
        )
        oauth.user = user
        db.session.add_all([user, oauth])
        db.session.commit()
        login_user(user)
        flash("Successfully signed in with Google.")

    print(f"Logged in user: {current_user.name}, {current_user.email}")
    return False

# notify on OAuth provider error
@oauth_error.connect_via(blueprint)
def google_error(blueprint, error, error_description=None, error_uri=None):
    msg = (
        "OAuth error from {name}! "
        "error={error} description={description} uri={uri}"
    ).format(
        name=blueprint.name,
        error=error,
        description=error_description,
        uri=error_uri,
    )
    flash(msg, category="error")

if __name__ == "__main__":
    if "--setup" in sys.argv:
        with app.app_context():
            db.create_all()
            db.session.commit()
            print("Database tables created")
    else:
        app.run(debug=True)