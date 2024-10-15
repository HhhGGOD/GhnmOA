from flask import Blueprint, request, jsonify, session
import pandas as pd
import os
import re

auth_blueprint = Blueprint('auth', __name__)

users_file = 'users.xlsx'

# 确保用户数据文件存在
if not os.path.exists(users_file):
    df = pd.DataFrame(columns=['username', 'password'])
    df.to_excel(users_file, index=False)


@auth_blueprint.route('/login', methods=['POST'])
def login_user():
    
    data=request.get_json()
    username = data.get('username','').strip()
    password = data.get('password','').strip()

    df = pd.read_excel(users_file)
    # print("Users in Excel:", df) 

    # print(f"Looking for username: {username} and password: {password}")
    user = df[(df['username'] == username) & (df['password'] == password)]
    # print(f"User found: {not user.empty}")  # 查看是否找到了用户


    if not username or not password:
        return jsonify({"error": "Username or password not provided"}), 400
    
    # print(f"Received username: {username}, password: {password}")
    
    if user.empty:
        return jsonify({"error": "用户名或密码错误"}), 401

    session['username'] = username
    return jsonify({"message": "登录成功"}), 200


@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # if data is None:
    #     return jsonify({'error': '请求体为空或格式错误'}), 408
    # else: 
    #     print("接收到的数据:", data)  # 输出接收到的 JSON 数据
    username = data.get('username')
    password = data.get('password')

    df = pd.read_excel(users_file)

    if not re.match(r'^[A-Za-z].*', username):
        return jsonify({'error': '必须以字母开头!'}), 400

    if username in df['username'].values:
        return jsonify({'error': '用户名已存在!'}), 400

    if not username or not password:
        return "用户名和密码不能为空", 402

    new_user = pd.DataFrame({'username': [username], 'password': [password]})
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_excel(users_file, index=False)

    return jsonify({'message': '注册成功!'}), 201
