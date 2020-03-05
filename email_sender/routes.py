# coding: utf-8
# Konstantyn Davidenko


from flask import request, render_template, redirect, url_for, Blueprint, flash
from flask_login import login_required
from email_sender.forms import InstantSendEmailForm, SchedulerSendForm
from models import Document

email_bp = Blueprint('email_sender', __name__, template_folder='templates')


@email_bp.route('send_document/<document_id>', methods=['GET', 'POST'])
@login_required
def instant_send(document_id: int):
    form = InstantSendEmailForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.send_mail(document_id=document_id)
            return redirect(url_for('documents.index'))
        else:
            flash('invalid data')
    document = Document.query.get(document_id)
    return render_template('send_email/send_email.html', document=document, form=form)


@email_bp.route('send_periodic/<document_id>', methods=['GET', 'POST'])
def send_periodic(document_id):
    form = SchedulerSendForm(request.form)
    document = Document.query.get(document_id)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.add_task(document_id)
            return redirect(url_for('documents.index'))
    return render_template('send_email/periodic_send.html', document=document, form=form)

