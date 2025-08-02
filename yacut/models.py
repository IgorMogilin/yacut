from datetime import datetime
import random
from http import HTTPStatus

from yacut import db

from .constants import (
    ERROR_INVALID_CUSTOM_ID,
    MAX_ATTEMPT_GENERATE,
    MAX_ORIGINAL_LINK_LENGTH,
    SHORTLINK_ALLOWED_CHARS,
    SHORTLINK_MAX_LENGTH,
    SHORTLINK_VALID_RE,
    SHORT_LINK_ALREADY_EXIST,
    SHORT_STANDART_LENGTH,
    COULD_NOT_GENERATE_SHORTLINK
)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_LINK_LENGTH), nullable=False)
    short = db.Column(
        db.String(SHORTLINK_MAX_LENGTH),
        nullable=False,
        unique=True
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @classmethod
    def get(cls, short_id):
        return cls.query.filter_by(short=short_id).first()

    @classmethod
    def get_unique_short_id(
        cls,
        length=SHORT_STANDART_LENGTH,
        max_attempts=MAX_ATTEMPT_GENERATE
    ):
        for _ in range(max_attempts):
            short_id = ''.join(
                random.choice(SHORTLINK_ALLOWED_CHARS) for _ in range(length)
            )
            if not cls.get(short_id):
                return short_id
        raise RuntimeError(
            COULD_NOT_GENERATE_SHORTLINK,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )

    def save(self):
        if self.short:
            if (
                len(self.short) > SHORTLINK_MAX_LENGTH
                or not SHORTLINK_VALID_RE.fullmatch(self.short)
            ):
                raise ValueError(ERROR_INVALID_CUSTOM_ID)
            if URLMap.get(self.short):
                raise ValueError(SHORT_LINK_ALREADY_EXIST)
        else:
            self.short = URLMap.get_unique_short_id()
        db.session.add(self)
        db.session.commit()