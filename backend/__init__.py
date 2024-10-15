from flask import Flask
from .auth import auth_blueprint

def create_app():
    app = Flask(__name__)
    app.secret_key = '12138'  # 设置密钥以使用闪存消息

    # 注册蓝图
    app.register_blueprint(auth_blueprint)

    return app
