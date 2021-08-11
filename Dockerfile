from python:3.7-slim

copy ./requirements.txt /tmp/requirements.txt

run pip install --no-cache-dir -r /tmp/requirements.txt

# build the wheel and install
# TODO: create a multistage build with the wheel as output
workdir /package-install
copy ./package .
run pip install .
