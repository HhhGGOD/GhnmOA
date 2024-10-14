from flask import Flask, send_from_directory, request, jsonify, session, render_template
from werkzeug.security import generate_password_hash
import os
from backend import app, db, User
from backend.auth import auth_blueprint 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__,static_folder='frontend/static',template_folder='frontend')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = '12138'
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)

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
    # 登录逻辑
    pass

@app.route('/register', methods=['POST'])
def register():
    # 注册逻辑
    pass

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
        db.create_all()  # 创建数据库表
    app.run(host='0.0.0.0', port=5000, debug=True)
