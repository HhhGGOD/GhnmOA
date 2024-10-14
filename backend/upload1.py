from flask import Blueprint, request, jsonify
import os

upload1_blueprint = Blueprint('upload1', __name__)
upload1_folder = 'uploads1'
os.makedirs(upload1_folder, exist_ok=True)

@upload1_blueprint.route('/upload1', methods=['POST'])
def upload1_file():
    if 'file' not in request.files:
        return jsonify({"error": "文件未上传"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "未选择文件"}), 400

    filepath = os.path.join(upload1_folder, file.filename)
    file.save(filepath)

    return jsonify({"message": "文件上传成功", "filename": file.filename}), 200