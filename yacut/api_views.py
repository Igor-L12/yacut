import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .models import URLMap
from .utils import get_unique_short_id

SHORT_LINK = "http://localhost/"
REGEX = r"^[a-zA-Z\d]{1,16}$"


@app.route("/api/id/", methods=["POST"])
def create_short_url():
    data = request.get_json()

    if not data:
        return (
            jsonify({"message": "Отсутствует тело запроса"}),
            HTTPStatus.BAD_REQUEST,
        )

    if "url" not in data:
        return (
            jsonify({"message": '"url" является обязательным полем!'}),
            HTTPStatus.BAD_REQUEST,
        )

    if "custom_id" not in data or not data["custom_id"]:
        short_id = get_unique_short_id()
    else:
        short_id = data["custom_id"]

    if URLMap.query.filter_by(short=short_id).first():
        return (
            jsonify({"message": f'Имя "{short_id}" уже занято.'}),
            HTTPStatus.BAD_REQUEST,
        )

    if short_id and (len(short_id) > 15 or not re.match(REGEX, short_id)):
        return (
            jsonify(
                {
                    "message": "Указано недопустимое имя для короткой ссылки"
                }
            ),
            HTTPStatus.BAD_REQUEST,
        )

    url_map = URLMap(original=data["url"], short=short_id)
    db.session.add(url_map)
    db.session.commit()

    return (
        jsonify(
            {
                "url": url_map.original,
                "short_link": f"{SHORT_LINK}{url_map.short}"
            }
        ),
        HTTPStatus.CREATED,
    )


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_short_url_info(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is not None:
        return jsonify({"url": url_map.original})
    return jsonify({"message": "Указанный id не найден"}), HTTPStatus.NOT_FOUND
