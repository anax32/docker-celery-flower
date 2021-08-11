from fastapi import FastAPI

from myapp.worker.main import celery_app
from myapp.worker import fast, slow


app = FastAPI()


@app.get("/")
def get_index():
  return {"status": "ok"}


@app.post("/fast-worker")
def start_fast_worker():
  # kick off a job and wait for the result
  result = fast.add.delay(4, 4).get()
  # return the result
  return {"status": "ok", "result": result}


@app.post("/slow-worker")
def start_slow_worker():
  # kick of a job and ignore it
  task = slow.add.delay(4, 4)
  id = task.task_id
  # poll for results later
  return {"status": "ok", "id": id}


@app.get("/tasks")
def get_tasks():
  """check the status on tasks"""
  i = celery_app.control.inspect()

  return {
      "status": "ok",
      "tasks": {
          "scheduled": i.scheduled(),
          "active": i.active(),
          "reserved": i.reserved()
      }
  }

@app.get("/tasks/{id}")
def get_task_information(id: str):
  """get status of a specific task"""
  from celery.result import AsyncResult as CeleryResult

  r = CeleryResult(id, backend=celery_app.backend)

  info = {
    "id": id,
    "info": r.info,
    "status": r.status,
    "name": r.name,
  }

  return info
