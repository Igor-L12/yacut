import os
import string

VALID_SYMBOLS_SHORT_LINK = string.ascii_letters + string.digits
MAX_ORIGINAL_LENGTH = 2048
MAX_SHORT_LENGTH = 16

CUSTOM_ID_REGEX = r'^[a-zA-Z0-9_]+$'

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='SECRET_KEY')
