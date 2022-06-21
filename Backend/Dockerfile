# Pull base image
FROM python:3.10.2-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# creating working directory
RUN mkdir -p /home/ubuntu/Backend/

# Set work directory
WORKDIR /home/ubuntu/Backend/

# copying all file to docker working directory
COPY . .

# updating linux os
RUN apt-get update

# install dependency for postgresql
RUN apt-get install -y postgresql libpq-dev postgresql-client postgresql-client-common gcc

# installing pipenv
RUN pip install pipenv

# installing app dependency
RUN pipenv install --system --deploy --ignore-pipfile


