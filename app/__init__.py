from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mysecrectkey_123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///samadhan.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.__init__(app)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app