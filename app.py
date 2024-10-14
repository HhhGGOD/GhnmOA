from flask import Flask, send_from_directory
from backend.upload import upload_blueprint
from backend.process import process_blueprint
from backend.download import download_blueprint


app = Flask(__name__,static_folder='frontend/static')


app.config['SECRET_KEY'] = '12138'
app.config['UPLOAD_FOLDER'] = 'uploads'


# 注册蓝图
app.register_blueprint(upload_blueprint)
app.register_blueprint(process_blueprint)
app.register_blueprint(download_blueprint)


@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/filter')
def filter_page():
    return send_from_directory('frontend', 'filter.html')

@app.route('/visualize')
def visualize_page():
    return send_from_directory('frontend', 'visualize.html')

@app.route('/file_share')
def file_share_page():
    return send_from_directory('frontend', 'file_share.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
