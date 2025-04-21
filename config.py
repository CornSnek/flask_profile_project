import os
basedir = os.path.abspath(os.path.dirname(__file__))
class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(BaseConfig):
    SECRET_KEY = "TODO_NON_PROPER_NOT_HARDCODED_SECURITY_KEY"
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"

class ProductionConfig(BaseConfig):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")