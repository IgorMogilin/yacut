import re

SHORTLINK_MIN_LENGTH = 1
SHORTLINK_MAX_LENGTH = 16
SHORTLINK_VALID_RE = re.compile(r'^[A-Za-z0-9]{1,16}$')
SHORT_LINK_ALREADY_EXIST = (
    'Предложенный вариант короткой ссылки уже существует.'
)
NO_REQUEST_BODY = 'Отсутствует тело запроса'
ERROR_NO_URL_FIELD = '"url" является обязательным полем!'
ERROR_INVALID_CUSTOM_ID = 'Указано недопустимое имя для короткой ссылки'
ERROR_ID_NOT_FOUND = 'Указанный id не найден'