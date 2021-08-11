import os

from celery import Celery

celery_app = Celery(
    "myapp",
    include=["myapp.worker.slow", "myapp.worker.fast"]
)
