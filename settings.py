import os
import re
import string

VALID_SYMBOLS_SHORT = string.ascii_letters + string.digits
MAX_ORIGINAL_LENGTH = 2048
MAX_SHORT_LENGTH = 16
REDIRECT_VIEW_NAME = 'redirect_view'
SHORT_REGEX = rf'^[{re.escape(VALID_SYMBOLS_SHORT)}]+$'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI',
                                        default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='SECRET_KEY')
