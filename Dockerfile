FROM python:3.8.8
ENV PYTHONUNBUFFERED=1
RUN python3 -m pip install --upgrade pip
RUN apt-get update \
    && apt-get install -y postgresql postgresql-contrib gcc python3-dev musl-dev
WORKDIR /django
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

