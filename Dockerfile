FROM python:3.6-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install pipenv -y
RUN pip install --upgrade pip

COPY Pipfile* /tmp/

RUN cd /tmp && pipenv lock --requirements > /tmp/requirements.txt
RUN pip install --upgrade -r /tmp/requirements.txt

COPY ./restaurant /app/

CMD python manage.py runserver 0.0.0.0:8000

EXPOSE 8000
