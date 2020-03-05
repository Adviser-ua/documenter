# coding: utf-8
# Konstantyn Davidenko

from flask import Blueprint, render_template
from models import Document

documents_bp = Blueprint('documents', __name__, template_folder='templates')


@documents_bp.route('/')
def index():
    documents = Document.query.all()
    return render_template('documents/documents.html', documents=documents)
