from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import pandas as pd
from factory import TaskFactory
from utils.logs import logger

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
        # Start automation process
        start_automation(file_path)
        return jsonify({'message': 'File successfully uploaded and processed'}), 200

def start_automation(file_path):
    try:
        # Read the spreadsheet
        df = pd.read_excel(file_path)
        # For simplicity, assuming the first row contains the data to be processed
        row = df.iloc[0]
        
        task = TaskFactory.create_task('register_process', row)
        task.execute()
        logger.info('Process successfully registered.')
    except Exception as e:
        logger.error(f'Error processing the file: {e}')

if __name__ == '__main__':
    app.run(debug=True)

