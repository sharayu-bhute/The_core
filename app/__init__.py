from flask import Flask, app 
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'mysecrectkey_123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///samadhan.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = False

    db.init_app(app)

    from app.routes.auth import auth_bp, admin_bp
    from app.routes.complaint import complaint_bp
    app.register_blueprint(complaint_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    return app