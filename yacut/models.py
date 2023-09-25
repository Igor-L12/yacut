import random
import re
from datetime import datetime

from flask import url_for

from settings import (CUSTOM_ID_REGEX, MAX_ORIGINAL_LENGTH, MAX_SHORT_LENGTH,
                      VALID_SYMBOLS_SHORT_LINK)

from . import db

NAME_ALREADY_USE_ERROR = 'Имя {name} уже занято!'
INVALID_NAME_ERROR = 'Указано недопустимое имя для короткой ссылки'


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
        return url_for('redirect_view', short=self.short, _external=True)

    @staticmethod
    def get_unique_short_id(length=6):
        short_id = ''.join(random.choice(VALID_SYMBOLS_SHORT_LINK)
                           for _ in range(length))
        if not URLMap.find_by_short(short=short_id):
            return short_id

    @staticmethod
    def find_by_short(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create_new_url(original_link, custom_id=None):
        if custom_id:
            if len(custom_id) > MAX_SHORT_LENGTH:
                raise ValueError(INVALID_NAME_ERROR)
            if not re.match(CUSTOM_ID_REGEX, custom_id):
                raise ValueError(INVALID_NAME_ERROR)
            existing_url = URLMap.find_by_short(custom_id)
            if existing_url:
                raise Exception(NAME_ALREADY_USE_ERROR.format(name=custom_id))
        if not custom_id:
            custom_id = URLMap.get_unique_short_id()
        url_map = URLMap(original=original_link, short=custom_id)
        db.session.add(url_map)
        db.session.commit()

        return url_map
