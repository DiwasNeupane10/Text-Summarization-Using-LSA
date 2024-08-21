import magic
upload_folder='./uploads'

def allowed_files(file):
    allowed_extensions={'txt','pdf','docx'}
    allowed_mimetypes={'application/vnd.openxmlformats-officedocument.wordprocessingml.document','application/pdf','text/plain'}
    if not('.' in file.filename and \
           file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        return False
    file_chunks=file.read(1024)
    file_mime = magic.from_buffer(file_chunks, mime=True)
    file.seek(0)  # Reset file pointer
    if file.filename.rsplit('.', 1)[1].lower() in allowed_extensions and file_mime=='application/zip':
        return True
    # return file_mime
    return file_mime in allowed_mimetypes


