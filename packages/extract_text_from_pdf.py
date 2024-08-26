from pypdf import PdfReader
from werkzeug.utils import secure_filename
import os
import docx
def extract_text(file):
    extension=file.filename.rsplit('.',1)[1].lower()
    # if file.filename.rsplit('.',1)[1].lower() =='.pdf':
    text=[]
        # reader=PdfReader(file)
    match extension:
        case 'pdf':
            try:
                reader=PdfReader(file)
                for page_no in (range(len(reader.pages))):
                    page=reader.pages[page_no]
                    text.append(page.extract_text())

                filename=secure_filename(file.filename.rsplit('.',1)[0])+'.txt'
                path=os.path.join('./extraction',filename)
                with open(path,'w',encoding='utf-8') as f:
                    for line in text:
                        if line:
                            f.write(line)
                            f.write('\n\n')
            except Exception as e:
                raise ValueError("Text extraction Failed") from e

        case 'docx':
                try:
                    doc = docx.Document(file)
                    fullText = []
                    for para in doc.paragraphs:
                        fullText.append(para.text)
                    text.append('\n'.join(fullText))

                    filename=secure_filename(file.filename.rsplit('.',1)[0])+'.txt'
                    path=os.path.join('./extraction',filename)
                    with open(path,'w',encoding='utf-8') as f:
                        for line in text:
                            if line:
                                f.write(line)
                except Exception as e:
                    raise ValueError("Text Extraction Failed") from e
                            # f.write('\n\n')
        case _:
            pass
        

        