import os

from celery import Celery

celery_app = Celery(
    "myapp",
    include=["myapp.worker.slow", "myapp.worker.fast"]
)


async def create_state_monitor(app):
  """create a celery state monitor which runs in the background

  https://docs.celeryproject.org/en/stable/userguide/monitoring.html#custom-camera
  """
  import asyncio

  state = app.events.State()

  async def celery_state_listener():
    with app.connection() as connection:
      recv = app.events.Receiver(
          connection,
          handlers={'*': state.event}
      )

      while True:
        recv.capture(limit=10, timeout=None)
        await asyncio.sleep(2.0)

  asyncio.create_task(celery_state_listener())

  return state


async def parse_state_to_dict(state):
  """parse a state object to a dict

  we use this instead of the .info() or __repr__() or
  serializers included in celery because they do not
  propagate the event params sent with send_event() and
  typically are full of nulls.

  We want the event params

  state: celery.state.State object
  returns: dict [uuid, task info]
  """
  ignore_fields = [
      "cluster_state",
      "children",
      "_serializer_handlers",
      "root",
      "parent",
      "worker"
  ]

  # FIXME: we can't serialise the Task object because of
  # the State enum field which is stored in the Task.__dict__
  # field (we only want the __dict__). So we have to filter here
  return {uuid: {k: v for k, v in task.__dict__.items()
          if k not in ignore_fields}
          for uuid, task in state.tasks_by_time()}
