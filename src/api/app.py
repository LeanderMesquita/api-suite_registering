from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import pandas as pd
from factory import TaskFactory
from utils.functions.error_report import error_report
from utils.functions.click_and_fill import click_and_fill
from utils.functions.successfully_report import successfully_report
from utils.logger.logger import log



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
        df = pd.read_excel(file_path)
        if not (df.empty): log.success('Dataframe create sucessfully!')
        for index, row in df.iterrows():
            try:
                log.info(f'Registering process: ({row['NUMERO DO PROCESSO']}).')
                situational_init_key = 'novo_processo' if index == 0 else 'processo_seguinte'
                click_and_fill(situational_init_key)
                task = TaskFactory.create_task('author', row)
                task.execute()
                log.success(f'Process ({row['NUMERO DO PROCESSO']}) was registered with success!')
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

