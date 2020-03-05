# coding: utf-8
# Konstantyn Davidenko

import uuid
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email

from app import db
from models import AsyncTask, PeriodicTask, Document
from tasks import send_async_email


PERIOD_CHOICE = (
    ("minute", "minute"),
    ("second", "second"),
    ("hour", "hour"),
    ("day", "day"),
    ("month", "month")
)


class InstantSendEmailForm(FlaskForm):

    receiver = EmailField('Email address', [DataRequired(), Email()])
    submit = SubmitField('Send')

    def send_mail(self, document_id):
        task_id = str(uuid.uuid4())
        ps = AsyncTask(receiver=self.receiver.data, document_id=document_id, task_id=task_id)
        db.session.add(ps)
        db.session.commit()
        send_async_email.apply_async((self.receiver.data, ps.id), task_id=task_id)


class SchedulerSendForm(FlaskForm):
    receiver = EmailField('Email address', [DataRequired(), Email()])
    start_send = DateField('start send')
    end_send = DateField('end send')
    submit = SubmitField('Send')
    period_type = SelectField('period type', choices=PERIOD_CHOICE)
    period_value = StringField("period")

    def add_task(self, document_id):
        task_id = str(uuid.uuid4())
        task = PeriodicTask(
            receiver=self.receiver.data,
            document_id=document_id,
            task_id=task_id,
            start_sent=self.start_send.data,
            end_sent=self.end_send.data,
            period_type=self.period_type.data,
            period_value=self.period_value.data
        )
        db.session.add(task)
        db.session.commit()
        # todo add run schedule task
