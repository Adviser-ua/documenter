# coding: utf-8
# Konstantyn Davidenko

import os
from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # SECURITY CONFIGURATION
    SECRET_KEY = 'its-not-funny'
    UPLOAD_FOLDER = os.path.join(basedir, 'upload')

    # FLASK-MAIL CONFIGURATION
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'kostyamail05@gmail.com'
    MAIL_PASSWORD = '********'
    MAIL_DEFAULT_SENDER = 'kostyamail05@gmail.com'
    ADMINS = ['kostyamail05@gmail.com']

    # CELERY CONFIGURATION
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    CELERY_TIMEZONE = 'Europe/Warsaw'

    CELERYBEAT_SCHEDULE = {
        'my_scheduled_job': {
            'task': 'run_scheduled_jobs',
            'schedule': crontab(minute='*'),
        },
    }
    # DATABASE CONFIGURATION
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(basedir, 'app.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
