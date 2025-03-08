import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect,
    send_from_directory,
    flash,
    url_for,
    session,
)
# import dotenv
# # dotenv.load_dotenv()

from flask_session import Session
from werkzeug.utils import secure_filename

from packages.allowed_file import FileVerifier
from packages.allowed_file import upload_folder

from packages.extract_text_from_files import TextExtractor

from packages.preprocessing_text import TextPreProcessor

# from packages.calc_TF_IDF import CustomTFIDF

# from packages.svd import CustomSVD
from packages.date_time import get_date_time


from packages.sentence_scoring import SentenceSelection
from packages.clear_directory import clear_dir
from packages.LSA import LSA


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = upload_folder
app.secret_key = "textsummarizer123"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST", "GET"])
def handle_files():
    if request.method == "POST":
        file_verifier_object=FileVerifier()
        if "file" not in request.files:
            return jsonify({"error": "No file part in the request"})

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No selected file"})


        elif file and file_verifier_object.check_allowed_files(file):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            
            text_extractor_object=TextExtractor()
            flag, path = text_extractor_object.extract_text(file)
            if flag:
                session["path"] = path
                return jsonify(
                    {"message": "File successfully uploaded and Text is extracted"}
                )
            else:
                return jsonify({"error": "Failure text cannot be extracted"})
           

        else:
            return jsonify({"error": "File type not allowed"})

    else:
        clear_dir("extraction")
        return render_template("upload.html")


@app.route("/summary", methods=["GET", "POST"])
def summarization():
    if request.method == "POST":
        input_type = request.form["input_type"]  # get the value of the input
        summary_length = int(request.form["length"])
        #create a textpreprocessor object
        preprocessor_object=TextPreProcessor()
        clear_dir("summary")
        if input_type == "textarea":
            # if the user chooses to provide input from the text area
            user_text = request.form["text_area"]  # get the text from the textarea with name text_area
            preprocessed_sentences,tokenized_sentences,index_map= preprocessor_object.preprocessor(user_text)
            

            if not preprocessed_sentences:
                flash("Error:Input format is incorrect")#meaning the input is not in English
                return redirect(url_for("index"))

            elif len(preprocessed_sentences) <= summary_length:#check for the summary length 
                flash("Error:Input text must be longer than the summary length")
                return redirect(url_for("index"))
            #create a LSA object
            LSA_object=LSA(preprocessed_sentences)
            U,_,_=LSA_object.process()#returns U,sigma,vt but we only need U matrix so _ is used to specify that
            #create a sentence selection objet
            Sentence_selection_object=SentenceSelection(U,preprocessed_sentences,tokenized_sentences,summary_length, index_map)
            
            summary=Sentence_selection_object.cross(preprocessor_object.sentence_to_indices)
            current_date = get_date_time()
            path = os.path.join("./summary", f"summary_{current_date}.txt")
            with open(path, "w", encoding="utf-8") as f:
                for sent in summary:
                    f.write(sent[0])
                    f.write("\n")
            #get the summary score data 
            session["score_data"] = {"score": [sent[1] for sent in summary]}
            #store the summary path in the session
            session["s_path"] = path
            return redirect(url_for("summarization"))

        elif input_type == "fileup":
            #if the user chooses  file as the input
            #check if the path keyword is in the session and if it exists then check if the path exists in the system
            if "path" not in session or not os.path.exists(session["path"]):
                flash("Error Upload File Again")
                return redirect(url_for("handle_files"))

            with open(session["path"], "r", encoding="utf-8") as f:
                file_text = f.read()
            (
                preprocessed_sentences,
                tokenized_sentences,
                index_map,
            ) = preprocessor_object.preprocessor(file_text)
            if not preprocessed_sentences:
                flash("Error:Incorrect input format")
                return redirect(url_for("index"))
            elif len(preprocessed_sentences) <= summary_length:
                flash("Error:Input sentences  must be more than the summary length")
                return redirect(url_for("handle_files"))
            LSA_object=LSA(preprocessed_sentences)
            U,_,_=LSA_object.process()
           
            Sentence_selection_object=SentenceSelection(U,preprocessed_sentences,tokenized_sentences,summary_length, index_map)
            summary=Sentence_selection_object.cross(preprocessor_object.sentence_to_indices)
            current_date = get_date_time()
            path = os.path.join("./summary", f"summary_{current_date}.txt")
            with open(path, "w", encoding="utf-8") as f:
                for sent in summary:
                    f.write(str(sent[0].replace("\n", "").replace("\r", "")))
                    f.write("\n")
            session["s_path"] = path
            session["score_data"] = {"score": [sent[1] for sent in summary]}
            clear_dir("extraction")
            clear_dir("uploads")
            return redirect(url_for("summarization"))

    else: 
        #if the request method is other than post
        if not "s_path" in session:
            #check if the user naviagtes to summary route without the generated summary
            flash("Error: No summary data")
            return redirect(url_for("index"))
        #open the generatedd summary file
        with open(session["s_path"], "r", encoding="utf-8") as f:
            display_summary = [
                line.replace("\n", "") for line in f.readlines() if line.strip()
            ]

        if not display_summary:
            flash("Error: No summary data")
            return redirect(url_for("index"))
        #get the summary score
        display_score = session.get("score_data")
        display_score = list(display_score.values())[0]#convert to list
        summary_data = [
            (d_summary, d_score)
            for d_summary, d_score in zip(display_summary, display_score)
        ]#creates a tuple for the each sentence and its associated
        session.pop("path", None)
        session.pop("s_path", None)
        session.pop("score_data", None)
        #clear the session data
        return render_template("summarization.html", summary_data=summary_data)


@app.route("/download_file", methods=["GET", "POST"])
def handle_download():
    if request.method == "GET":
        return redirect("/")
    else:
        dir = os.listdir("./summary")
        dir.remove(".gitkeep")
        return send_from_directory("./summary", dir[0], as_attachment=True)


@app.route("/summary_api", methods=["POST"])
def summarization_api():
    if not request.is_json:
        return jsonify({"error": "Invalid input, JSON expected"})
    preprocessor_object=TextPreProcessor()
    data = request.get_json()
    expected_types = {"summary_length": int, "text": str}
    errors = validate_json(data, expected_types)
    if errors:
        return jsonify({"errors": errors})
    for key in data.keys():
        if key == "summary_length":
            length = int(data["summary_length"])
        elif key == "text":
            text = data["text"]
    (
        preprocessed_sentences,
        tokenized_sentences,
        index_map,
    ) = preprocessor_object.preprocessor(text)
    if not preprocessed_sentences:
        return jsonify({"error": "Incorrect Input Format"})
    elif len(preprocessed_sentences) < length:
        return jsonify({"error": "Summary length should be less than input length"})
    
    LSA_object=LSA(preprocessed_sentences)
    U,_,_=LSA_object.process()
    
    Sentence_selection_object=SentenceSelection(U,preprocessed_sentences,tokenized_sentences,length, index_map)
    summary=Sentence_selection_object.cross(preprocessor_object.sentence_to_indices)
    summarized_sentences = [
        str(sent[0]).replace("\n", "").replace("\r", "") for sent in summary
    ]
    scores = [sent[1] for sent in summary]
    return jsonify({"summary": summarized_sentences, "scores": scores})


def validate_json(data, expected_types):
    errors = []
    for key, expected_type in expected_types.items():
        if key not in data:
            #expected types consists of the key and the values the api expects 
            errors.append(f"Missing field: {key}")
        elif not isinstance(data[key], expected_type): #check for the value got from the request is instance of the expected type
            errors.append(
                f"Incorrect type for field '{key}': expected {expected_type.__name__}, got {type(data[key]).__name__}"
            )
    return errors


if __name__ == "__main__":
    app.run(debug=True)
