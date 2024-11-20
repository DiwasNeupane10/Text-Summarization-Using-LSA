import os
from flask import Flask,render_template,jsonify,request,redirect,send_from_directory
from werkzeug.utils import secure_filename
from packages.allowed_file import allowed_files
from packages.allowed_file import upload_folder
from packages.extract_text_from_files import extract_text
from packages.preprocessing_text import preprocessor
from packages.calc_TF_IDF import compute_tf_idf
from packages.svd import calc_svd
from packages.date_time import get_date_time
# from packages.sentence_scoring import calc_sentence_score,calc_rank
from packages.sentence_scoring import cross
from packages.word_scoring import cross_words

app=Flask(__name__)
app.config['UPLOAD_FOLDER']=upload_folder

@app.route("/",methods=['GET','POST'])
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
    


@app.route('/summary',methods=['GET','POST'])
def summarization():
    if request.method=='POST':
        input_type=request.form['input_type']#get the value of the input
        summary_length=request.form['length']
        dir_summ=os.listdir('./summary')
        for dir in dir_summ:
            if dir!='.gitkeep':
                os.remove(os.path.join('./summary',dir))
        if input_type=='textarea':
            user_text=request.form['text_area']#get the text from the textarea with name text_area
            preprocessed_sentences,tokenized_sentences,index_map,tokenized_words,word_index_map=preprocessor(user_text)
            # print(tokenized_sentences)
            # tf,isf,tf_idf=compute_tf_idf(preprocessed_sentences)
            tf_idf=compute_tf_idf(preprocessed_sentences)
            tf_idf_array=tf_idf.to_numpy()
            sh=tf_idf_array.shape
            # tf,isf,tf_idf=tf.to_html(classes='table table-striped'),isf.to_html(classes='table table-striped',index=True),tf_idf.to_html(classes='table table-striped')
            # return render_template('summarization.html',table1=tf,table2=isf,table3=tf_idf)
            U,S,Vt=calc_svd(tf_idf_array)
            # print(f"{U.shape} {S.shape} {Vt.shape}")
            # u,s,vt=np.linalg.svd(tf_idf_array)
            # print(f"{u}{s}{vt}")
            # sentence_rank=calc_sentence_score(U,S,tokenized_sentences)
            # calc_rank(sentence_rank,tokenized_sentences,summary_length)
            summary=cross(U,tokenized_sentences,summary_length,index_map)
            words=cross_words(Vt,tokenized_words,word_index_map)
            current_date=get_date_time()
            path=os.path.join('./summary',f'summary_{current_date}.txt')
            with open(path,'w',encoding='utf-8') as f:
                for sent in summary:
                    f.write(sent)
                    f.write("\n")
            # print(sentence_rank)
            return render_template('summarization.html',summary=summary,words=words)
            # return render_template('summarization.html',U=U,S=S,Vt=Vt,sh=sh)
            # return render_template('summarization.html',tf_idf_array=tf_idf_array)
        elif input_type=='fileup':
            dir=os.listdir('./extraction')#return a list with all the files and folders
            preprocessed_sentences=[]
            dir.remove('.gitkeep')
            if dir:#if the directory is not empty 
                path=os.path.join('./extraction',dir[0])
                if os.path.exists(path):
                    with open(path,'r',encoding='utf-8') as f:
                        file_text=f.read()
                        preprocessed_sentences,tokenized_sentences,index_map,tokenized_words,word_index_map=preprocessor(file_text)
                # tf,isf,tf_idf=compute_tf_idf(preprocessed_sentences)
                tf_idf=compute_tf_idf(preprocessed_sentences)
                tf_idf_array=tf_idf.to_numpy()
                U,S,Vt=calc_svd(tf_idf_array)
                summary=cross(U,tokenized_sentences,summary_length,index_map)
                words=cross_words(Vt,tokenized_words,word_index_map)
                # sentence_rank=calc_sentence_score(U,tokenized_sentences)
                # calc_rank(sentence_rank,tokenized_sentences,summary_length)
                # tf,isf,tf_idf=tf.to_html(classes='table table-striped'),isf.to_html(classes='table table-striped',index=False),tf_idf.to_html(classes='table table-striped')
                # return render_template('summarization.html',table1=tf,table2=isf,table3=tf_idf)
                current_date=get_date_time()
                path=os.path.join('./summary',f'summary_{current_date}.txt')
                with open(path,'w',encoding='utf-8') as f:
                    for sent in summary:
                        f.write(sent)
                        f.write("\n")

                dir_ex=os.listdir('./extraction')
                for dir in dir_ex:
                    if dir!='.gitkeep':
                        os.remove(os.path.join('./extraction',dir))
                dir_up=os.listdir('./uploads')
                for dir in dir_up:
                    if dir!='.gitkeep':
                        os.remove(os.path.join('./uploads',dir))

                # return render_template('summarization.html',U=U,S=S,Vt=Vt)  
                return render_template('summarization.html',summary=summary,words=words)

            else:
                  return render_template('summarization.html',summary="Neither file Nor text input has been given .Go back!")
        
    else:
        return render_template('summarization.html',summary="Neither file Nor text input has been given .Go back!")

@app.route("/download_file",methods=['GET','POST'])
def handle_download():
    if request.method=="GET":
        return redirect("/")
    else:
        dir=os.listdir("./summary")
        dir.remove('.gitkeep')
        return send_from_directory('./summary',dir[0],as_attachment=True)
if __name__ == '__main__':

    app.run(debug=True)