"""
task inherits from celery.Task to provide callback notifications and
track progress.

This example loops until 100 random numbers have been generated which
are > threshold. Each valid value calls send_event to add data to the
flower dashboard.
"""
import celery

from myapp.worker.main import celery_app

from random import random
from time import sleep


class MyAppTask(celery.Task):
  name = "myapp-task"
  track_started = True

  def __init__(self):
    """seems we can use init and it is not used by the celery.Task class
       so we don't need a super() call
    """
    pass

  def run(self, threshold=0.9):
    """run this function on task.delay()...

       if __call__ this is specified, the run() function is ignored, however,
       __call__ sets up a bunch of stuff and calls run(), which then throws
       a NotImplementedError if it is not defined, so we are better off using
       run() when implemented our callback.

       this specific function just runs random and every 100 times
       random() > threshold, we send a progress event to the logger
       via Task.send_event
    """
    iter = 0
    count = 100

    while iter<count:
      if random() > threshold:
        iter = iter+1
        self.send_event("task-progress", current=iter, total=count)

      sleep(0.1)


  def after_return(self, status, retval, task_id, args, kwargs, einfo):
    """Handler called after the task returns.
       https://docs.celeryproject.org/en/4.0/userguide/tasks.html#after_return
       https://docs.celeryproject.org/en/4.0/reference/celery.app.task.html#celery.app.task.Task.after_return
    """
    pass

  def on_failure(self, exc, task_id, args, kwargs, einfo):
    """This is run by the worker when the task fails.
       https://docs.celeryproject.org/en/4.0/userguide/tasks.html#on_failure
       https://docs.celeryproject.org/en/4.0/reference/celery.app.task.html#celery.app.task.Task.on_failure
    """
    pass

  def on_retry(self, exc, task_id, args, kwargs, einfo):
    """This is run by the worker when the task is to be retried.
       https://docs.celeryproject.org/en/4.0/userguide/tasks.html#on_retry
       https://docs.celeryproject.org/en/4.0/reference/celery.app.task.html#celery.app.task.Task.on_retry
    """
    pass

  def on_success(self, retval, task_id, args, kwargs):
    """Run by the worker if the task executes successfully.
       https://docs.celeryproject.org/en/4.0/userguide/tasks.html#on_success
       https://docs.celeryproject.org/en/4.0/reference/celery.app.task.html#celery.app.task.Task.on_success
    """
    pass

# register the task
celery_app.tasks.register(MyAppTask())
