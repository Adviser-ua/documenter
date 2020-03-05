import os

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from config import Config

# flask app
app = Flask(__name__)
app.config.from_object(Config)


# async task
def make_celery(app: Flask):
    # create context tasks in celery
    celery = Celery(
        app.import_name,
        broker=Config.CELERY_BROKER_URL,
        backend=Config.CELERY_RESULT_BACKEND
    )
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    celery.conf.beat_schedule = Config.CELERYBEAT_SCHEDULE
    return celery


celery = make_celery(app)

# mail
mail = Mail()
mail.init_app(app)

# database
db = SQLAlchemy(app)
login = LoginManager(app)
login.init_app(app)
login.login_view = "auth.login"
migrate = Migrate(app, db)


# load components
from auth.routes import auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

from loader.routes import loader_bp
app.register_blueprint(loader_bp, url_prefix='/loader')

from document_creator.routes import creator_bp
app.register_blueprint(creator_bp, url_prefix='/create')

from email_sender.routes import email_bp
app.register_blueprint(email_bp, url_prefix='/email_sender')

from task_status.routes import task_bp
app.register_blueprint(task_bp, url_prefix='/status')

from documents.routes import documents_bp
app.register_blueprint(documents_bp, url_prefix='/')

import models


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

