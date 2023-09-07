from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route("/", methods=["GET", "POST"])
def index_view():
    form = URLForm()

    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data

        existing_url = URLMap.query.filter_by(short=custom_id).first()
        if existing_url:
            flash(f"Имя {custom_id} уже занято!")
            return render_template("yacut.html", form=form)
        else:
            if not custom_id:
                custom_id = get_unique_short_id()

            url_map = URLMap(original=original_link, short=custom_id)
            db.session.add(url_map)
            db.session.commit()

        return (
            render_template("yacut.html", form=form, short=custom_id),
            HTTPStatus.OK
        )

    return render_template("yacut.html", form=form)


@app.route("/<string:short>")
def redirect_view(short):
    url_map = URLMap.query.filter_by(short=short).first()
    if url_map is not None:
        return redirect(url_map.original)
    abort(404)


@app.route("/error_500")
def error_500_view():
    abort(500)
