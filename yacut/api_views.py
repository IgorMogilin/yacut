from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constants import ERROR_ID_NOT_FOUND, ERROR_NO_URL_FIELD, NO_REQUEST_BODY
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
    url_map.save()
    short_url = f"{request.host_url.rstrip('/')}/{url_map.short}"
    return jsonify({
        'url': url_map.original,
        'short_link': short_url
    }), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_shtortlink_link(short_id):
    url = URLMap.get(short_id=short_id)
    if not url:
        return jsonify({
            'message': ERROR_ID_NOT_FOUND
        }), HTTPStatus.NOT_FOUND
    return jsonify({'url': url.original}), HTTPStatus.OK
