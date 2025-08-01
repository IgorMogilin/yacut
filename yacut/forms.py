from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from .constants import (
    SHORTLINK_MAX_LENGTH,
    SHORTLINK_MIN_LENGTH,
    SHORTLINK_VALID_RE,
)


class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired('Обязательное поле'), URL()]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Optional(),
                    Length(min=SHORTLINK_MIN_LENGTH, max=SHORTLINK_MAX_LENGTH),
                    Regexp(SHORTLINK_VALID_RE)]
    )
    submit = SubmitField('Создать')
