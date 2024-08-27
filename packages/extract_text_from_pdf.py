from pypdf import PdfReader
from werkzeug.utils import secure_filename
import os
import docx
def extract_text(file):
    extension=file.filename.rsplit('.',1)[1].lower() # splits the file name from the right after encountering the first '.'.[1].lower means converting the extension to lowercase
    flag=True
    text=[]
    
    match extension:
        case 'pdf':
            try:
                reader=PdfReader(file) #read the file
                for page_no in (range(len(reader.pages))):
                    page=reader.pages[page_no]
                    text.append(page.extract_text())

                filename=secure_filename(file.filename.rsplit('.',1)[0])+'.txt' #after spliting the filename takes the filename and adds extension of'.txt'
                path=os.path.join('./extraction',filename)
                with open(path,'w',encoding='utf-8') as f:
                    for line in text:
                        if line:
                            f.write(line)
                            f.write('\n\n')
                with open(path,'r',encoding='utf-8') as f:
                    content=f.read().strip()
                    if  not bool(content):
                    
                        flag=not flag
                if flag:
                    return flag
                else :
                    os.remove(path)
                    os.remove(os.path.join('./uploads',file.filename))
                    return flag

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
                with open(path,'r',encoding='utf-8') as f:
                    content=f.read().strip()
                    if  not bool(content):
                        flag=not flag
                if flag:
                    return flag
                
                else:
                    os.remove(path)
                    os.remove(os.path.join('./uploads',file.filename))
                    return flag
                    
            except Exception as e:
                raise ValueError("Text Extraction Failed") from e
                         
        case 'txt':
            try:
                filename=secure_filename(file.filename)
                open_path=os.path.join('./uploads',filename)
                with open(open_path,'r',encoding='utf-8') as f:
                    content=f.read().strip()
                    if  not bool(content):
                        return not flag
                    
                os.rename(open_path, os.path.join('./extraction', filename))
                return flag
            except Exception as e:
                raise ValueError("Text Extraction Failed") from e
            
        
        case _:
            pass
        

        