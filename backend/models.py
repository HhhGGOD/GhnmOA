from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 用户角色

class SharedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    allowed_roles = db.Column(db.String(120), nullable=False)  # 可访问用户角色
