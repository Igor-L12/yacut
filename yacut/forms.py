from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

ORIGINAL_LINK_LABEL = 'Введите оригинальную ссылку'
CUSTOM_ID_LABEL = 'Введите ваш вариант ссылки'
SUBMIT_LABEL = 'Создать'
MISSING_FIELD = 'Обязательное поле'
ERROR_SYMBOLS = 'Недопустимые символы в ссылке'
MAX_ORIGINAL_LINK_LENGTH = 2048
MAX_CUSTOM_ID_LENGTH = 16

CUSTOM_ID_REGEX = r'^[a-zA-Z0-9_-]+$'

class URLForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_LABEL,
        validators=[
            DataRequired(message=MISSING_FIELD),
            Length(max=MAX_ORIGINAL_LINK_LENGTH)
        ]
    )
    custom_id = StringField(
        CUSTOM_ID_LABEL,
        validators=[
            Length(max=MAX_CUSTOM_ID_LENGTH),
            Optional(),
            Regexp(CUSTOM_ID_REGEX, message=ERROR_SYMBOLS)
        ]
    )
    submit = SubmitField(SUBMIT_LABEL)
