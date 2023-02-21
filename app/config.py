from datetime import timedelta
class Config:
    UPLOAD_FOLDER="./profile_pic_uploads"
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=5)
    SECRET_KEY="664qHCBhBhG1bKK6"
    SALT = "46c^"
    MYSQL_USER="admin"
    MYSQL_PASSWORD="programmer"
    MYSQL_DB="WRKR_MGM"
