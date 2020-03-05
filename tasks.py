# coding: utf-8
# Konstantyn Davidenko

from flask_mail import Message
from app import celery, app, mail, db
from models import Document, AsyncTask
import mimetypes
import datetime


@celery.task(name='send_email', bind=True)
def send_async_email(self, receiver: str, planing_send_id: int):
    """Background task to send an email_sender with Flask-Mail."""
    async_task, doc = db.session.query(AsyncTask, Document).join(Document).filter(AsyncTask.id == planing_send_id).first()
    try:
        with app.open_resource(doc.file) as fp:
            print(f'send: {async_task.id}')
            message = ''
            subject = 'instant mail'
            msg = Message(recipients=[receiver], body=message, subject=subject)
            mime_type, encode = mimetypes.guess_type(doc.file)
            msg.attach(doc.filename, mime_type, fp.read())
            mail.send(msg)
            async_task.sent = True
            async_task.day_send = datetime.datetime.now()
            async_task.detail = 'success'
            db.session.add(async_task)
            db.session.commit()
    except Exception as e:
        async_task.detail = str(e)
        db.session.add(async_task)
        db.session.commit()


@celery.task(name='run_scheduled_jobs')
def run_scheduled_jobs():
    print(f'beat still works: {datetime.datetime.now()}')
    return True
