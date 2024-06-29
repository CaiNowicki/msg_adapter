from flask import Flask, send_file, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
import re

app = Flask(__name__, static_url_path='/static')
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DESKTOP-P2UO69O\SQLEXPRESS/AnimorphsSite?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # limits uploads to 16 MB

#create the uploads folder if does not exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        # check to make sure post request has file and filename in it
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
    
        file = request.files['file']
        if file.filename == "":
            flash('No selected file')
            return redirect(request.url)
        
        # user has selected a file
        if file:
            #save file
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            #send file to dummy backend
            result = process_file(filepath)
            return render_template('result.html', result=result)
    return render_template('index.html')

def process_file(filepath):
    #TODO: function to convert .msg files to .txt files or string or JSON or something
    #for demo purposes, returning a fixed number
    return 42

if __name__ == '__main__':
    app.run()
