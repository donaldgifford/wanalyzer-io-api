import os

from celery import Celery

from app.core.get_top_20 import load_data
from app.db.base import SessionLocal

celery = Celery()
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")


@celery.task()
def update_data():
    load_data(db=SessionLocal())
    return True
