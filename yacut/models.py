import random
import re
from datetime import datetime

from flask import url_for

from settings import (MAX_ORIGINAL_LENGTH, MAX_SHORT_LENGTH,
                      REDIRECT_VIEW_NAME, SHORT_REGEX, VALID_SYMBOLS_SHORT)

from . import db

NAME_ALREADY_USE_ERROR = 'Имя "{name}" уже занято.'
INVALID_NAME_ERROR = 'Указано недопустимое имя для короткой ссылки'
INVALID_ORIGINAL_URL = 'Указан недопустимый url!'
FAILED_GENERATE_LINK = 'Ошибка при генерации ссылки.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.get_short_url(),
        )

    def get_short_url(self):
        return url_for(REDIRECT_VIEW_NAME, short=self.short, _external=True)

    @staticmethod
    def get_unique_short_id(length=6):
        short = ''.join(random.choices(VALID_SYMBOLS_SHORT, k=length))
        if not URLMap.get(short=short):
            return short
        raise ValueError(FAILED_GENERATE_LINK)

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create(original_link, short=None, validate=False):
        if validate:
            if len(original_link) > MAX_ORIGINAL_LENGTH:
                raise ValueError(INVALID_ORIGINAL_URL)
            if short:
                if len(short) > MAX_SHORT_LENGTH:
                    raise ValueError(INVALID_NAME_ERROR)
                if not re.match(SHORT_REGEX, short):
                    raise ValueError(INVALID_NAME_ERROR)
        if not short:
            short = URLMap.get_unique_short_id()
        elif URLMap.get(short=short):
            raise ValueError(
                NAME_ALREADY_USE_ERROR.format(name=short))
        url_map = URLMap(original=original_link, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
