from flask import Blueprint, send_file

download_blueprint = Blueprint('download', __name__)

@download_blueprint.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_file(filename, as_attachment=True)
