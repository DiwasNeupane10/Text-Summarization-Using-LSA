upload_folder='./uploads'

def allowed_files(filename):
    allowed_extensions={'txt','pdf','docx'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions