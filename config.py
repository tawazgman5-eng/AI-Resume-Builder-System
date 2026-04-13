import os

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:yourpassword@localhost/resume_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)

class Config:
    DEBUG = True
    SECRET_KEY = 'your_secret_key'
