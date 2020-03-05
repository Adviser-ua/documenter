# coding: utf-8
# Konstantyn Davidenko

from flask import render_template, Blueprint
from flask_login import login_required

from app import db
from tasks import send_async_email
from models import AsyncTask, Document

task_bp = Blueprint('task_status', __name__, template_folder='templates')


@task_bp.route('tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    result = db.session.query(AsyncTask, Document).join(Document).all()
    return render_template('task_status/tasks.html', title='tasks', result=result)


@task_bp.route('task/<task_id>', methods=['GET', 'POST'])
@login_required
def task_status(task_id: str):
    task = send_async_email.AsyncResult(task_id)
    return render_template('task_status/task_status.html', title='tasks', task=task)
