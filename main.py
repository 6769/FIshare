#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

from flask import Flask, render_template, request, url_for, send_from_directory, redirect
from guestbook import *
from flask_dropzone import Dropzone
from datetime import datetime




app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()+'/upload'


app.config.update(
    DROPZONE_MAX_FILE_SIZE=500,
)

dropzone = Dropzone(app)
print(os.getcwd())
try:
    photos_list = os.listdir(app.config['UPLOAD_FOLDER'])
except FileNotFoundError:
    os.mkdir(app.config['UPLOAD_FOLDER'])
    photos_list = []

@app.route('/')
def index():
    greeting_list = load_data()
    files_list = os.listdir(app.config['UPLOAD_FOLDER'])
    files_list.sort()
    return render_template('index.html', 
                        files_list=files_list, 
                        greeting_list=greeting_list)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/', methods=['POST'])
def upload_file():
    
    file = request.files['file']
    if file:
        filename = file.filename
        print(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = url_for('uploaded_file', filename=filename, _external=True)
        return render_template('index.html') + file_url



@app.route('/delete/<filename>')
def delete_file(filename):
    file_path = './upload/'+filename
    os.remove(file_path)
    files_list = os.listdir(app.config['UPLOAD_FOLDER'])
    return redirect('/')

    
    
@app.route('/post', methods=['POST'])
def post():
    """Comment's target url
    """
    comment = request.form.get('comment')
    if( 0 == len(comment.split())):
        return redirect('/')
    create_at = datetime.now().ctime()
    save_data(comment, create_at)
    return redirect('/')

@app.route('/deletemsg/<msgindex>')
def delete_msg(msgindex):
    delete_data(msgindex)
    return redirect('/')


if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)