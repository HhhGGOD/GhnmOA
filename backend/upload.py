from flask import Blueprint, request, jsonify, session
import os

upload_blueprint = Blueprint('upload', __name__)
upload_folder = 'uploads'
os.makedirs(upload_folder, exist_ok=True)

@upload_blueprint.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "文件未上传"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "未选择文件"}), 400

    user_role = session.get('role')
    user_folder = os.path.join(upload_folder, user_role)

    os.makedirs(user_folder, exist_ok=True)
    
    filepath = os.path.join(user_folder, file.filename)
    file.save(filepath)

    return jsonify({"message": "文件上传成功", "filename": file.filename}), 200
