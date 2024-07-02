from flask import Flask, send_file, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
import re
import extract_msg
import random

app = Flask(__name__, static_url_path='/static')
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DESKTOP-P2UO69O\SQLEXPRESS/AnimorphsSite?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # limits uploads to 16 MB
app.config['SECRET_KEY'] = 'your_secret_key'

#create the uploads folder if does not exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text_data = request.form.get('text_data', '')
        files = request.files.getlist('files')

        # Validate that at least one input is provided
        if not text_data and not files:
            return render_template('index.html', error='Please upload a file or enter some text.')

        # Handle file if provided
        file_results = []
        if files:
            for file in files:
                if file.filename != "":
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                    file.save(filepath)
                    if filepath.endswith('.msg'):
                        file_result = process_msg_file(filepath)
                        file_results.append(file_result)
                    else:
                        file_results.append((f"Unsupported file type: {file.filename}", None))

        # Handle text if provided
        text_result = None
        if text_data:
            text_result = process_text(text_data)


        return render_template('result.html', file_results=file_results, text_result=text_result, text_data=text_data)

    return render_template('index.html')

def process_msg_file(filepath):
    #function to convert .msg files to string
    # TODO: hand off string to backend (JSON?)
    # then analyze text given for keywords, sentiment, and urgency
    #for demo purposes, returning a fixed number
    msg = extract_msg.Message(filepath)
    subject = msg.subject
    body = msg.body
    sender = msg.sender

    urgency_metric = round(random.uniform(1.0, 5.0), 1) # dummy value, to be replaced later, generates a random float in the range 1-5
    return urgency_metric, sender, subject, body

def process_text(text_data):
    #TODO: hand off text from box in the same format as process_file for same kind of analysis
    #for demo purposes, returning a fixed number
    return 2.4

if __name__ == '__main__':
    app.run()
