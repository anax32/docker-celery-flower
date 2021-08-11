import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

exec(open("myapp/version.py").read())

setuptools.setup(
    name="myapp-celery-example",
    version=__version__,
    author="ed",
    author_email="anax@hotmail.co.uk",
    description="FastAPI + workers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anax32/celery-example",
    packages=[
        "myapp",
        "myapp.api",
        "myapp.worker",
        "myapp.tests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "celery[redis]",
        "fastapi",
        "gunicorn",
        "uvicorn"
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "mock"],
    test_suite="myapp.tests",
)
