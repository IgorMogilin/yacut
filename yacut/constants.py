import re
import string

SHORTLINK_MIN_LENGTH = 1
SHORTLINK_MAX_LENGTH = 16
SHORT_STANDART_LENGTH = 6
MAX_ORIGINAL_LINK_LENGTH = 512
MAX_ATTEMPT_GENERATE = 100
SHORTLINK_VALID_RE = re.compile(
    f'^[A-Za-z0-9]{{{SHORTLINK_MIN_LENGTH},{SHORTLINK_MAX_LENGTH}}}$'
)
SHORTLINK_ALLOWED_CHARS = string.ascii_letters + string.digits
SHORT_LINK_ALREADY_EXIST = (
    'Предложенный вариант короткой ссылки уже существует.'
)
NO_REQUEST_BODY = 'Отсутствует тело запроса'
ERROR_NO_URL_FIELD = '"url" является обязательным полем!'
ERROR_INVALID_CUSTOM_ID = 'Указано недопустимое имя для короткой ссылки'
ERROR_ID_NOT_FOUND = 'Указанный id не найден'
COULD_NOT_GENERATE_SHORTLINK = 'Невозможно сгенерировать новую короткую ссылку'
