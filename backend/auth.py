from flask import Blueprint, request, jsonify, session
from .models import db, User
from werkzeug.security import generate_password_hash

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "用户名已存在"}), 409

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "注册成功"}), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        session['username'] = user.username
        session['role'] = user.role
        return jsonify({"message": "登录成功"}), 200
    return jsonify({"error": "用户名或密码错误"}), 401
