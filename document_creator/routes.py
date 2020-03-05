# coding: utf-8
# Konstantyn Davidenko

from flask import request, render_template, redirect, url_for
from flask_login import login_required
from document_creator.forms import NewDocumentForm

from flask import Blueprint
creator_bp = Blueprint('create', __name__, template_folder='templates')


@creator_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_document():
    form = NewDocumentForm()
    if request.method == 'GET':
        return render_template('document_creator/create_document.html', title='create document', form=form)
    if form.validate_on_submit():
        form.create_document()
        form.save()
        return redirect(url_for('documents.index'))
    return render_template('document_creator/create_document.html', title='create document', form=form)
