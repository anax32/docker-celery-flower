from myapp.worker.main import celery_app


@celery_app.task
def add(x, y):
  """add two numbers together and return"""
  return x + y
