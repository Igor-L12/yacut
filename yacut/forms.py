from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLForm(FlaskForm):
    original_link = URLField(
        'Введите оригинальную ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 2048)]
    )
    custom_id = StringField(
        'Введите ваш вариант ссылки',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Создать')
