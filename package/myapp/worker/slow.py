from myapp.worker.main import celery_app

@celery_app.task
def add(x, y, time_delay=20):
  """add two numbers together and delay for a period

  time_delay: number of seconds to delay return
  """
  from time import sleep
  sleep(time_delay)
  return x + y
