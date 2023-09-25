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
    custom_id = form.custom_id.data

    try:
        url_map = URLMap.create_new_url(original_link, custom_id)
    except Exception as error:
        flash(str(error))
        return render_template("index.html", form=form)

    return render_template(
        "index.html",
        form=form,
        short_url=url_map.get_short_url()
    ), HTTPStatus.OK


@app.route("/<string:short>")
def redirect_view(short):
    url_map = URLMap.find_by_short(short)
    if url_map:
        return redirect(url_map.original)
    abort(404)
