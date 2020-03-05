# coding: utf-8
# Konstantyn Davidenko


from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(1024), unique=True)
    filename = db.Column(db.String(120))


class AsyncTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receiver = db.Column(db.String(120), index=True)
    document_id = db.Column('document', db.Integer, db.ForeignKey('document.id'), nullable=False)
    task_id = db.Column(db.String(100))
    day_send = db.Column(db.DateTime)
    sent = db.Column(db.Boolean(), default=False)
    detail = db.Column(db.String)

    def __repr__(self):
        return '<AsyncTask {}>'.format(self.id)


class PeriodicTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receiver = db.Column(db.String(120), index=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    task_id = db.Column(db.String(100))
    start_sent = db.Column(db.DateTime)
    end_sent = db.Column(db.DateTime)
    period_type = db.Column(db.String(120), nullable=False)
    period_value = db.Column(db.String(20))
