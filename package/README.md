# myapp package documentation

this package handles the API specification and processing via `fastapi`
and the worker code called by `celery` in the subpackages:
+ `.api`
+ `.worker`

these could be in completely separate packages, but is not required.
We bundle everything together in the same package for brevity.
We could also have everything in a single python file, but that might
be a little too cluttered.
