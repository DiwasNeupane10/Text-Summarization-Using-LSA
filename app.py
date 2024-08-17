import os
from flask import Flask,render_template,jsonify,request
from werkzeug.utils import secure_filename
from packages.allowed_file import allowed_files
from packages.allowed_file import upload_folder

app=Flask(__name__)
app.config['UPLOAD_FOLDER']=upload_folder

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/", methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_files(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File successfully uploaded'}), 200
    
    return jsonify({'error': 'File type not allowed'}), 400


if __name__ == '__main__':
    app.run(debug=True)