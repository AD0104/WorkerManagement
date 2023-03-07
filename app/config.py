from datetime import timedelta
class Config:
    UPLOAD_FOLDER="./profile_pic_uploads"
    DOWNLOAD_FOLDER="./downloadable/files/pdf"
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=5)
