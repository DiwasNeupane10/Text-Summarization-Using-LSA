import os
from flask import Flask,render_template,jsonify,request
from werkzeug.utils import secure_filename
from packages.allowed_file import allowed_files
from packages.allowed_file import upload_folder
from packages.extract_text_from_pdf import extract_text

app=Flask(__name__)
app.config['UPLOAD_FOLDER']=upload_folder

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/upload", methods=['POST','GET'])
def handle_files():
    if request.method=='POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'})
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        
        # if file:
        #     return jsonify({'message':allowed_files(file)})  
        
        elif file and allowed_files(file):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # try:
            if extract_text(file):
                return jsonify({'message': 'File successfully uploaded and Text is extracted'})
            else :
                return jsonify({'message': 'Failure'})
            # except ValueError  as e:
            #     return jsonify({'error':str(e)})
                
        else:
            return jsonify({'error': 'File type not allowed'})
       
    else:
        return render_template('upload.html')
    

if __name__ == '__main__':
    app.run(debug=True)