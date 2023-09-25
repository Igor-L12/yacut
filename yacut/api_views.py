from http import HTTPStatus
from flask import jsonify, request
from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


ID_NOT_FOUND = 'Указанный id не найден'
REQUEST_MISSING_ERROR = 'Отсутствует тело запроса'
URL_FIELD_ERROR = '"url" является обязательным полем!'


@app.route("/api/id/", methods=["POST"])
def create_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(REQUEST_MISSING_ERROR)
    if 'url' not in data or not data['url']:
        raise InvalidAPIUsage(URL_FIELD_ERROR)
    custom_id = data.get('custom_id')
    if custom_id:
        existing_url = URLMap.find_by_short(custom_id)
        if existing_url:
            return (jsonify({"message": f'Имя "{custom_id}" уже занято.'}),
                    HTTPStatus.BAD_REQUEST,)
    try:
        return jsonify(URLMap.create_new_url(
            data['url'],
            custom_id
        ).to_dict()), HTTPStatus.CREATED
    except ValueError as error:
        raise InvalidAPIUsage(str(error))


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_short_url_info(short_id):
    url_map = URLMap.find_by_short(short=short_id)
    if not url_map:
        raise InvalidAPIUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({"url": url_map.original}), HTTPStatus.OK
