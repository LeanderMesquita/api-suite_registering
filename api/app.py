from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import pandas as pd
from api.src.factory import TaskFactory
from api.src.utils.functions.error_report import error_report
from api.src.utils.functions.click_and_fill import click_and_fill
from api.src.utils.functions.read_dataframe import read_dataframe
from api.src.utils.functions.successfully_report import successfully_report
from api.src.utils.logger.logger import log



app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        start_automation(file_path)
        return jsonify({'message': 'File successfully uploaded and processed'}), 200

def start_automation(file_path):
    try:
        log.info('Starting automation')
        df = read_dataframe(file_path)
        if not (df.empty): log.success('Dataframe create sucessfully!')
        for index, row in df.iterrows():
            try:
                log.info(f'Registering process: ({row['NUMERO DO PROCESSO']}).')
                task = TaskFactory.create_task('register_process', row)
                task.execute()
                log.success(f'Process ({row['NUMERO DO PROCESSO']}) was registered with success!')
                if index >= len(df) - 1: log.warning(f'All process are readed, please verify the reports. Iterate qtn{len(df)}')
                successfully_report(row['NUMERO DO PROCESSO'], row['AUTOR'])
            except Exception as e:
                log.error(f'The process: ({row['NUMERO DO PROCESSO']}) was not registered. {e}')
                log.info('Moving on to the next process...')
                error_report(row['NUMERO DO PROCESSO'], row['AUTOR'], error=e)
                continue
    except Exception as e:
        log.critical(f"An critical error occurred!: {e}")
         

if __name__ == '__main__':
    app.run(debug=True)
