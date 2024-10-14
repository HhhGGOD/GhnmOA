from flask import Flask
from .models import db, User
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()  # 创建数据库表

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
