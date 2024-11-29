from app import app
from signin import signin

app.register_blueprint(signin)


if __name__ == '__main__':
    app.run(debug=True)