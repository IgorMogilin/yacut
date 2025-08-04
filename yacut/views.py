from flask import abort, flash, redirect, render_template, url_for

from . import app
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index():
    """Вьюфункция для отображения главной страницы."""
    form = URLForm()
    if form.validate_on_submit():
        short_url = URLMap(
            original=form.original_link.data,
            short=form.custom_id.data
        )
        try:
            URLMap.save(short_url)
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('index'))
        flash(url_for(
            'redirect_view',
            short_id=short_url.short,
            _external=True
        ), 'short_link')
    return render_template('yacut.html', form=form)


@app.route('/<short_id>')
def redirect_view(short_id):
    """Вьюфункция для редиректа по короткой ссылке."""

    url = URLMap.get(short_id) or abort(404)
    return redirect(url.original)