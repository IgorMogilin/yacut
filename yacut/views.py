from flask import flash, redirect, render_template, url_for

from yacut import db

from . import app
from .constants import SHORT_LINK_ALREADY_EXIST
from .forms import URLForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index():
    """Вьюфункция для отображения главной страницы."""

    form = URLForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data or get_unique_short_id()
        if URLMap.query.filter_by(short=custom_id).first():
            flash(SHORT_LINK_ALREADY_EXIST, 'error')
            return redirect(url_for('index'))
        short_url = URLMap(
            original=form.original_link.data,
            short=custom_id
        )
        db.session.add(short_url)
        db.session.commit()
        flash(url_for(
            'redirect_view',
            short_id=custom_id,
            _external=True
        ), 'short_link')
    return render_template('yacut.html', form=form)


@app.route('/<short_id>')
def redirect_view(short_id):
    """Вьюфункция для редиректа по короткой ссылке."""

    url = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url.original)