from pypdf import PdfReader
from werkzeug.utils import secure_filename
from packages.date_time import get_date_time
import os
import docx

class TextExtractor():
    def __init__(self):
        self.__extracted_text=[]
        self.__flag=True
    def extract_text(self,file):
        extension = file.filename.rsplit(".", 1)[1].lower()  # splits the file name from the right after encountering the first '.'.[1].lower means converting the extension to lowercase
        match extension:
            case "pdf":
                try:
                    reader = PdfReader(file)  # read the file
                    for page_no in range(len(reader.pages)):
                        page = reader.pages[page_no]
                        self.__extracted_text.append(page.extract_text())
                    current_date_time = get_date_time()
                    filename = (secure_filename(file.filename.rsplit(".", 1)[0] + "_" + current_date_time) + ".txt")  # after spliting the filename takes the filename and adds extension of'.txt'
                    path = os.path.join("./extraction", filename)  # path for the extracted test to be save at
                    # writing the extracted text in a text file
                    with open(path, "w", encoding="utf-8") as f:
                        for line in self.__extracted_text:
                            if line:
                                f.write(line)
                                f.write("\n\n")
                    # Checking whether the extracted text is empty or not
                    with open(path, "r", encoding="utf-8") as f:
                        content = (f.read().strip())  # reads the file and strips the whitespaces from it
                        if not bool(content):  # bool(content) return true if there is text in the content
                            # and if it is false return false
                            self.__flag = not self.__flag
                    if self.__flag:
                        return self.__flag, path
                    else:
                        # if empty remove the original uploaded and extracted text file
                        os.remove(path)
                        os.remove(os.path.join("./uploads", file.filename))
                        return self.__flag, "Null"

                except Exception as e:
                    raise ValueError("Text extraction Failed") from e
            case "docx":
                    try:
                        doc = docx.Document(file)
                        paragraph_text = []
                        for para in doc.paragraphs:
                            paragraph_text.append(para.text)
                        self.__extracted_text.append("\n".join(paragraph_text))
                        current_date_time = get_date_time()
                        filename =secure_filename(file.filename.rsplit(".", 1)[0] + "_" + current_date_time)+".txt"
                        path = os.path.join("./extraction", filename)
                        with open(path, "w", encoding="utf-8") as f:
                            for line in self.__extracted_text:
                                if line:
                                    f.write(line)
                        with open(path, "r", encoding="utf-8") as f:
                            content = f.read().strip()
                            if not bool(content):
                                self.__flag = not self.__flag
                        if self.__flag:
                            return self.__flag, path

                        else:
                            os.remove(path)
                            os.remove(os.path.join("./uploads", file.filename)) 
                            return self.__flag,"Fail"

                    except Exception as e:
                        raise ValueError("Text Extraction Failed") from e
            case "txt":
                try:
                    filename = secure_filename(file.filename)
                    open_path = os.path.join("./uploads", filename)
                    with open(open_path, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                        if not bool(content):
                            return not self.__flag, "fail"
                    # for text files if there is content in it then change its directory straight to extracted folder
                    current_date_time = get_date_time()
                    new_path = os.path.join(
                        "./extraction",
                        filename.rsplit(".", 1)[0] + "_" + current_date_time + ".txt",
                    )
                    os.rename(open_path, new_path)
                    return self.__flag, new_path
                except Exception as e:
                    raise ValueError("Text Extraction Failed") from e

            case _:
                pass    






