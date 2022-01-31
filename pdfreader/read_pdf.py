from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from pdfreader.database.db import get_db

bp = Blueprint('read', __name__)


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/text')
def pdf_list():
    db = get_db()
    posts = db.execute(
        'SELECT id, pdf_name'
        ' FROM pdf_content '
        ' ORDER BY id ASC'
    ).fetchall()
    return render_template('liste.html', posts=posts)

@bp.route('/text/<int:id>')
def read_pdf(id):
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, author, uploaded, body'
        ' FROM pdf_content p WHERE p.id=(?)', (id,)
    ).fetchall()
    return render_template('text.html', posts=posts)