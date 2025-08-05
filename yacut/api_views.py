from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constants import (
    ERROR_ID_NOT_FOUND,
    ERROR_NO_URL_FIELD,
    NO_REQUEST_BODY,
    ERROR_INVALID_CUSTOM_ID,
    SHORT_LINK_ALREADY_EXIST,
    COULD_NOT_GENERATE_SHORTLINK
)
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_shortlink():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage(NO_REQUEST_BODY)
    if 'url' not in data:
        raise InvalidAPIUsage(ERROR_NO_URL_FIELD)
    url_map = URLMap(original=data['url'], short=data.get('custom_id'))
    try:
        url_map.save()
    except ValueError as e:
        raise InvalidAPIUsage(str(e)) from e
    except RuntimeError as e:
        raise InvalidAPIUsage(
            str(e),
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        ) from e

    short_url = f"{request.host_url.rstrip('/')}/{url_map.short}"
    return jsonify({
        'url': url_map.original,
        'short_link': short_url
    }), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_shortlink(short_id):
    url = URLMap.get(short_id=short_id)
    if not url:
        raise InvalidAPIUsage(
            ERROR_ID_NOT_FOUND,
            status_code=HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': url.original}), HTTPStatus.OK