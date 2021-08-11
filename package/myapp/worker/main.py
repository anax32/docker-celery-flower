import os

from celery import Celery


celery_app = Celery(
    "myapp",
    broker=os.environ["MYAPP_BROKER_URI"],
    backend=os.environ["MYAPP_BACKEND_URI"],
    include=["myapp.worker.slow", "myapp.worker.fast"]
)
