from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app
from .forms import URLForm
from .models import URLMap


@app.route("/", methods=["GET", "POST"])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template("index.html", form=form)
    original_link = form.original_link.data
    short = form.custom_id.data
    try:
        url_map = URLMap.create(original_link, short=short)
    except ValueError:
        flash(f'Имя {short} уже занято!')
        return render_template("index.html", form=form)
    return render_template(
        "index.html",
        form=form,
        short_url=url_map.get_short_url()
    ), HTTPStatus.OK


@app.route("/<string:short>")
def redirect_view(short):
    url_map = URLMap.get(short)
    if url_map:
        return redirect(url_map.original)
    abort(404)
