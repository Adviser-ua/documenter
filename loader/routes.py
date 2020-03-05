# coding: utf-8
# Konstantyn Davidenko

from flask import request, render_template, redirect, url_for
from flask_login import login_required
from flask import Blueprint
from loader.forms import UploadForm

loader_bp = Blueprint('loader', __name__, template_folder='templates')


@loader_bp.route('upload_file', methods=['GET', 'POST'])
@login_required
def upload_file():
    form = UploadForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            form.save()
            return redirect(url_for('documents.index'))
    return render_template('loader/upload_file.html', form=form)