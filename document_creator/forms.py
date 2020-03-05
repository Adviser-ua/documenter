# coding: utf-8
# Konstantyn Davidenko

import os
import uuid

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired
import pdfkit

from app import db, app
from models import Document

FILE_TYPE_CHOICES = (
    ("csv", "csv"),
    ("pdf", "pdf")
)


class NewDocumentForm(FlaskForm):
    document_type = SelectField('document type', choices=FILE_TYPE_CHOICES)
    document_name = StringField('document name', validators=[DataRequired()])
    document_text = TextAreaField('document_text', validators=[DataRequired()])
    document_path = ''
    submit = SubmitField('Create')

    def get_doc_path(self):
        unique_filename = str(uuid.uuid4())
        return os.path.join(app.config['UPLOAD_FOLDER'], 'created', unique_filename + '.' + self.document_type.data)

    def create_csv(self, path, content):
        with open(path, 'w') as d:
            d.write(content)

    def create_pdf(self, name, content):
        pdfkit.from_string(content, name)

    def create_document(self):
        self.document_path = self.get_doc_path()
        if self.document_type.data == 'csv':
            self.create_csv(self.document_path, self.document_text.data)
        elif self.document_type.data == 'pdf':
            self.create_pdf(self.document_path, self.document_text.data)

    def save(self):
        doc = Document()
        doc.file = self.document_path
        doc.type = self.document_type.data
        doc.filename = self.document_name.data
        db.session.add(doc)
        db.session.commit()
