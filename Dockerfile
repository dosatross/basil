
FROM python:3.7-alpine

# Project Files and Settings
ARG PROJECT=basil
ARG PROJECT_DIR=/opt/${PROJECT}

COPY . PROJECT_DIR
WORKDIR PROJECT_DIR

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# virtualenv
RUN pip install virtualenv
RUN virtualenv env
RUN source env/bin/activate
COPY requirements.pip .
RUN pip install -r requirements.pip

# database migrations
python manage.py migrate

EXPOSE 8000
# CMD ["gunicorn", "-w 4", "main:basil"]


ENTRYPOINT ["python", "manage.py"]
CMD ["runserver","0.0.0.0:8000"]