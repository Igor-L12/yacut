from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from settings import MAX_ORIGINAL_LENGTH, MAX_SHORT_LENGTH, SHORT_REGEX

ORIGINAL_LINK_LABEL = 'Введите оригинальную ссылку'
CUSTOM_ID_LABEL = 'Введите ваш вариант ссылки'
SUBMIT_LABEL = 'Создать'
MISSING_FIELD = 'Обязательное поле'
ERROR_SYMBOLS = 'Недопустимые символы в ссылке'


class URLForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_LABEL,
        validators=[
            DataRequired(message=MISSING_FIELD),
            Length(max=MAX_ORIGINAL_LENGTH)
        ]
    )
    custom_id = StringField(
        CUSTOM_ID_LABEL,
        validators=[
            Length(max=MAX_SHORT_LENGTH),
            Optional(),
            Regexp(SHORT_REGEX, message=ERROR_SYMBOLS)
        ]
    )
    submit = SubmitField(SUBMIT_LABEL)
