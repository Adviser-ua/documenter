# coding: utf-8
# Konstantyn Davidenko
import os
import uuid

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

from app import db, app
from models import Document

FILE_TYPE_CHOICES = (
    ("csv", "csv"),
    ("pdf", "pdf")
)


class UploadForm(FlaskForm):

    filename = FileField('image', validators=[FileRequired()])
    submit = SubmitField('Upload')

    def save(self):
        doc = Document()
        unique_filename = str(uuid.uuid4())
        extension = self.filename.data.filename.split('.')[-1]
        doc.type = extension
        doc.file = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded', unique_filename + '.' + extension)
        doc.filename = self.filename.data.filename
        db.session.add(doc)
        try:
            self.filename.data.save(doc.file)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
