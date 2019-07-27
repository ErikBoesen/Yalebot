import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    # Suppress warnings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
