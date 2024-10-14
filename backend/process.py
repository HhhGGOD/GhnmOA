from flask import Blueprint, request, jsonify
import pandas as pd
import os

process_blueprint = Blueprint('process', __name__)
upload_folder = 'uploads'

@process_blueprint.route('/process', methods=['POST'])
def process_data():
    data = request.json
    filename = data['filename']
    choice = data['choice']
    custom_name = data['custom_name']

    filepath = os.path.join(upload_folder, filename)

    # 读取 Excel 文件
    if filename.endswith('.xlsx'):
        df = pd.read_excel(filepath, engine='openpyxl')
    else:
        df = pd.read_excel(filepath)

    # 根据选择筛选数据
    if choice == "option1":
        filtered_data = df[(df['总工资'] > 100000) & (df['总工资'] < 200000) & (df['级别'] < 5)]
    elif choice == "option2":
        filtered_data = df[(df['总工资'] > 200000) & (df['总工资'] < 250000)]
    elif choice == "option3":
        filtered_data = df[(df['总工资'] < 100000)]
    elif choice == "option4":
        filtered_data = df[(df['级别'] > 4)]

    # 计算工资的平均值
    avg_salary = filtered_data['总工资'].mean() if not filtered_data.empty else 0
    avg_row = pd.DataFrame({'薪资平均值': [avg_salary]})
    filtered_data = pd.concat([filtered_data, avg_row], ignore_index=True)

    # 导出处理后的数据
    output_file = f"{custom_name}.xlsx"
    filtered_data.to_excel(output_file, index=False)

    return jsonify({"download_link": output_file}), 200
