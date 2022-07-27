FROM python:3.9-alpine3.13
LABEL maintainer="londonappdeveloper.com"

ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

    # create virtual environment first
    # upgrade pip
    # install requirements.txt
    # remove tmp directory, we don't want any extra dependency on the image
    # add/create user, Do not run app using the root user,
RUN python -m venv /py && \ 
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# update the virture environment variable with default path
ENV PATH="/py/bin:$PATH"

# specify the user we switch to 
# so it should be the last line to set up for the docker image
USER django-user