
FROM python:3.7-alpine AS builder

COPY requirements.txt /
RUN apk add \
    --upgrade \
    --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
    postgresql-dev g++ python3-dev musl-dev py3-virtualenv py-pandas
    
RUN virtualenv -p python /var/basil/env
RUN /var/basil/env/bin/pip install --upgrade pip
RUN /var/basil/env/bin/pip install -r requirements.txt

FROM python:3.7-alpine
RUN apk add  \
    --upgrade \
    libpq libstdc++
COPY --from=builder /var/basil/env /var/basil/env
COPY . /opt/basil
WORKDIR /opt/basil
RUN /var/basil/env/bin/python -m compileall -q -f /opt/basil
EXPOSE 8000
ENTRYPOINT ["/var/basil/env/bin/gunicorn", "--chdir", "/opt/basil", "-c", "/opt/basil/gunicorn.py", "basil.wsgi:application"]