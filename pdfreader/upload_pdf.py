import functools
import PyPDF2
import json
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from pdfreader.database.db import get_db
from werkzeug.utils import secure_filename
import os
from flask import current_app
from pdfminer.high_level import extract_text

def parser(file):
    pdf_file = current_app.open_instance_resource(file, 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    info = read_pdf.getDocumentInfo()
    text = extract_text(pdf_file)

    # creator = info.creator
    # producer = info.producer
    # subject = info.subject
    
    author = json.dumps(info.author)
    title = json.dumps(info.title)
    metadata = json.dumps(info)
    file_content = json.dumps(text)


    return metadata,author,title,file_content


ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


bp = Blueprint('pdf', __name__, url_prefix='/documents')

@bp.route('/', methods=('GET', 'POST'))
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'pdf_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['pdf_file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('Aucun fichier selectionné')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            pdf = request.files["pdf_file"]
            pdf.save(os.path.join(current_app.config['TEMP']))
            data = parser('tempo.pdf')
            db = get_db()

            error = None

            if error is None:
                try:
                    db.execute(
                        "INSERT INTO pdf_content (metadata, author, title, body, pdf_name) VALUES (?,?,?,?,?)",
                        (data[0],data[1],data[2],data[3], filename), 
                    )
                    db.commit()
                    flash('Le PDF a bien été enregistré !')
                except db.IntegrityError:
                    error = f"Ce PDF {filename} est déjà enrégistré."
                    flash(error)
                else:
                    return redirect(request.url)
                return redirect(request.url)
            flash(error)

    return render_template('documents.html')