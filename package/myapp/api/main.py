"""Example FastAPI-to-Celery

## description

example API to invoke tasks executed by Celery

## usage

+ run the associated docker-compose file with `docker-compose up --build`
+ navigate to `http://localhost:8000/docs` to see the swagger interface to this API
+ also open `http://localhost:5555` to see the flower monitoring of the celery cluster
+ schedule some jobs using the API endpoints
    + `/fast-worker` is a fast 4+4 operation
    + `/slow-worker` is a slow 4+4 operation (sleep command)
    + `/random-worker` generates 100 random numbers greater than __n__
+ observe the jobs in the cluster with flower
+ get some job information from the API endpoints
    + `/tasks` is a list of workers and tasks running on those workers
    + `/tasks/<id>` gets information about a particular task (`id` is the return value from the long running jobs)

## implementation details

+ `/fast-worker` is a celery task where the caller waits for the return value with `task.get()`
+ `/slow-worker` is a celery task where the caller does not wait, but returns an ID so the client can request the information later
+ `/random-worker` is a celery task class, which allows callbacks on `return`, `success` and `failure`

The result storage **requires** that celery is configured with a backend: see
the `docker-compose.yaml` file for details on this.
"""
from fastapi import FastAPI

from myapp.worker.main import celery_app
from myapp.worker import fast, slow
from myapp.worker.callbacks import MyAppTask

from myapp import __version__ as myapp_version


tags_metadata = [
    {
        "name": "work",
        "description": "Tasks dispatched to worker nodes in the cluster.",
        "externalDocs": {
            "description": "Celery workers documentation",
            "url": "https://docs.celeryproject.org/en/stable/userguide/workers.html",
        },
    },
    {
        "name": "tasks",
        "description": "Information about running and completed tasks.",
        "externalDocs": {
            "description": "Celery tasks documentation",
            "url": "https://docs.celeryproject.org/en/stable/userguide/tasks.html"
        }

    },
]


app = FastAPI(
    title=__doc__.splitlines()[0],
    description="\n".join(__doc__.splitlines()[1:]),
    version=myapp_version,
    openapi_tags=tags_metadata
)


@app.get("/")
def get_index():
  return {"status": "ok"}


@app.post("/fast-worker", tags=["work"])
def start_fast_worker():
  # kick off a job and wait for the result
  result = fast.add.delay(4, 4).get()
  # return the result
  return {"status": "ok", "result": result}


@app.post("/slow-worker", tags=["work"])
def start_slow_worker():
  # kick of a job and ignore it
  task = slow.add.delay(4, 4)
  id = task.task_id
  # poll for results later
  return {"status": "ok", "id": id}


@app.post("/random-worker", tags=["work"])
def start_random_worker():
  task = MyAppTask()
  task_info = task.delay()

  # run the task directly by invoking the run command
  # task.run()
  return {"status": "ok", "id": task_info.task_id}


@app.get("/tasks", tags=["tasks"])
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


@app.get("/tasks/{id}", tags=["tasks"])
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
