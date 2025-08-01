from http import HTTPStatus

from flask import jsonify, request

from yacut import db

from . import app
from .constants import (
    ERROR_ID_NOT_FOUND,
    ERROR_INVALID_CUSTOM_ID,
    ERROR_NO_URL_FIELD,
    NO_REQUEST_BODY,
    SHORTLINK_MAX_LENGTH,
    SHORTLINK_VALID_RE,
    SHORT_LINK_ALREADY_EXIST,
)
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_shortlink():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage(NO_REQUEST_BODY)
    if 'url' not in data:
        raise InvalidAPIUsage(ERROR_NO_URL_FIELD)
    custom_id = data.get('custom_id')
    if custom_id:
        if (len(custom_id) > SHORTLINK_MAX_LENGTH or
                not SHORTLINK_VALID_RE.fullmatch(custom_id)):
            raise InvalidAPIUsage(ERROR_INVALID_CUSTOM_ID)
    if custom_id:
        if URLMap.query.filter_by(short=custom_id).first():
            return jsonify(
                {'message': SHORT_LINK_ALREADY_EXIST}
            ), HTTPStatus.BAD_REQUEST
    else:
        custom_id = get_unique_short_id()
    url = URLMap(original=data['url'], short=custom_id)
    db.session.add(url)
    db.session.commit()
    short_url = f"{request.host_url.rstrip('/')}/{custom_id}"
    return jsonify({
        'url': data['url'],
        'short_link': short_url
    }), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_shtortlink_link(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        return jsonify({
            'message': ERROR_ID_NOT_FOUND
        }), HTTPStatus.NOT_FOUND
    return jsonify({'url': url.original}), HTTPStatus.OK
