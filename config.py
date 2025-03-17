import os

from flask.cli import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "instance", "moviweb_app.db")


class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("The SECRET_KEY is not set! Please set it in your environment variables.")

    API_KEY = os.getenv("API_KEY")
    if not API_KEY:
        raise ValueError("The API_KEY is not set! Please set it in your environment variables.")

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
