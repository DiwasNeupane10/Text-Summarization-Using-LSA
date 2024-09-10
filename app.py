import os
from flask import Flask,render_template,jsonify,request,url_for
from werkzeug.utils import secure_filename
from packages.allowed_file import allowed_files
from packages.allowed_file import upload_folder
from packages.extract_text_from_files import extract_text
from packages.preprocessing_text import preprocessor

app=Flask(__name__)
app.config['UPLOAD_FOLDER']=upload_folder

@app.route("/",methods=['GET','POST'])
def index():
    if request.method=="POST":
        return url_for('summarization')
    else:
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
    


@app.route('/summary',methods=['GET','POST'])
def summarization():
    if request.method=='POST':
        input_type=request.form['input_type']#get the value of the input
        if input_type=='textarea':
            user_text=request.form['text_area']#get the text from the textarea with name text_area
            filtered_words=preprocessor(user_text)
            return render_template('summarization.html',text=filtered_words)
    else:
        filtered_words=[]
        dir=os.listdir('./extraction')#return a list with all the files and folders
        dir.remove('.gitkeep')
        if dir:#if the directory is not empty 
            path=os.path.join('./extraction',dir[0])
            if os.path.exists(path):
                with open(path,'r',encoding='utf-8') as f:
                    file_text=f.read()
                    filtered_words=preprocessor(file_text)
        if not filtered_words:
            return render_template('summarization.html',text="Neither file Nor text input has been given .Go back!")
        else:
            return render_template('summarization.html',text=filtered_words)    
            
    



if __name__ == '__main__':
    app.run(debug=True)