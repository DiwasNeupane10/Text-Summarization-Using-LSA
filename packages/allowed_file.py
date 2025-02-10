import magic

upload_folder = "./uploads"

class FileVerifier():
    def __init__(self):
        self.__allowed_extensions=["txt", "pdf", "docx"]
        self.__allowed_mimetypes = ["application/vnd.openxmlformats-officedocument.wordprocessingml.document","application/pdf","text/plain"]

    def check_allowed_files(self,file):
        if not ("." in file.filename and file.filename.rsplit(".", 1)[1].lower() in self.__allowed_extensions):
            return False
        file_chunks = file.read(1024)
        file_mime = magic.from_buffer(file_chunks, mime=True)
        file.seek(0)  # Reset file pointer
        if (file.filename.rsplit(".", 1)[1].lower() in self.__allowed_extensions and file_mime == "application/zip"):
            return True
    # return file_mime
        return file_mime in self.__allowed_mimetypes
        