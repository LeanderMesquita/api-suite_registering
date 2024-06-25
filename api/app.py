from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import pyautogui as pya
from api.src.exceptions.failsafe import FailSafeException
from api.src.factory import TaskFactory
from api.src.utils.functions.error_report import error_report
from api.src.utils.functions.click_and_fill import click_and_fill
from api.src.utils.functions.read_dataframe import read_dataframe
from api.src.utils.functions.successfully_report import successfully_report
from api.src.utils.logger.logger import log



app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        
        filename = secure_filename(file.filename)
        log.info(f'Received file: {filename}')
        df = read_dataframe(file)
        start_automation(df)
        
        return jsonify({'message': 'File successfully uploaded and processed'}), 200

def start_automation(df):
    try:
        log.info('Starting automation')
        if not (df.empty): log.success('Dataframe create sucessfully!')
        
        for index, row in df.iterrows():
            x, y = pya.position()
            if x == 0 and y == 0:
                raise FailSafeException('FAIL SAFE TRIGGERED')
            try:
                log.info(f'Registering process: ({row['NUMERO DO PROCESSO']}).')
                task = TaskFactory.create_task('register_process', row)
                task.execute()
                log.success(f'Process ({row['NUMERO DO PROCESSO']}) was registered with success!')
                if index >= len(df) - 1: log.warning(f'All process are readed, please verify the reports. Iterate qtn{len(df)}')
                successfully_report(row['NUMERO DO PROCESSO'], row['AUTOR'])
            except Exception as e:
                log.error(f'The process: ({row['NUMERO DO PROCESSO']}) was not registered. {e}')
                error_report(row['NUMERO DO PROCESSO'], row['AUTOR'], error=e)
                continue
    except Exception as e:
        log.critical(f"An critical error occurred!: {e}")
         

if __name__ == '__main__':
    app.run(host='0.0.0.0')

