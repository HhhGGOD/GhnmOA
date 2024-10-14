from flask import Flask, send_from_directory, request, jsonify, session, render_template
from werkzeug.security import generate_password_hash,check_password_hash
import os
from backend import create_app, db, User
from backend.auth import auth_blueprint 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app =create_app()

app = Flask(__name__,static_folder='frontend/static',template_folder='frontend')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = '12138'
app.config['UPLOAD_FOLDER'] = 'uploads'

from backend.auth import auth_blueprint
from backend.upload import upload_blueprint
from backend.upload1 import upload1_blueprint
from backend.download import download_blueprint
from backend.process import process_blueprint

# 注册蓝图
app.register_blueprint(auth_blueprint)
app.register_blueprint(upload_blueprint)
app.register_blueprint(upload1_blueprint)
app.register_blueprint(download_blueprint)
app.register_blueprint(process_blueprint)

@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/filter')
def filter_page():
    return send_from_directory('frontend', 'filter.html')

@app.route('/visualize')
def visualize_page():
    return send_from_directory('frontend', 'visualize.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    
    # 验证用户和密码
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id  # 登录会话
        return jsonify({"message": "登录成功"}), 200
    
    return jsonify({"error": "用户名或密码错误"}), 401


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # 检查用户名是否存在
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "用户名已存在"}), 400

    # 密码哈希
    hashed_password = generate_password_hash(password)

    # 创建新用户
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "注册成功"}), 201



@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/file_share')
def file_share_page():
    if 'username' in session:
        return send_from_directory('frontend', 'file_share.html')
    return send_from_directory('frontend', 'login.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'username' not in session:
        return jsonify({"error": "未登录"}), 403

    if 'file' not in request.files:
        return jsonify({"error": "没有文件上传"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "没有选择文件"}), 400

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return jsonify({"message": "文件上传成功!"})


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    if 'username' not in session:
        return jsonify({"error": "未登录"}), 403
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)



if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()  # 创建所有表
            user_count = db.session.query(User).count()  # 查询用户表中的记录数
            print(f"连接成功，当前用户数量: {user_count}")
        except Exception as e:
            print(f"数据库连接失败: {e}")

    app.run(host='0.0.0.0', port=5000, debug=True)
