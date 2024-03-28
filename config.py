from dotenv import load_dotenv
import os


load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///todos.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT')) if os.getenv('MAIL_PORT') else None
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    SECRET_KEY = 'your-secret-key'