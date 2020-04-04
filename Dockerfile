FROM nickgryg/alpine-pandas:3.7 AS builder
RUN apk add \
    --upgrade \
    --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
    postgresql-dev g++ python3-dev musl-dev py-pandas libffi-dev openssl-dev
COPY requirements.txt /
WORKDIR /wheels
RUN pip install -U pip && \
    pip wheel -r /requirements.txt


FROM python:3.7-alpine
RUN apk add  \
    --upgrade \
    libpq libstdc++
COPY --from=builder /wheels /wheels
COPY . /opt/basil
WORKDIR /opt/basil
RUN pip install -U pip && \
    pip install --no-cache-dir -r requirements.txt -f /wheels && \
    rm -rf /wheels && \
    ln -s /usr/local/bin /opt/basil/bin && \
    ln -s /usr/local/lib /opt/basil/lib && \
    python -m compileall -q -f /opt/basil
EXPOSE 8000
ENV BASIL_ENV production
ENV BASIL_DB_HOST basil-postgres
ENTRYPOINT ["gunicorn", "--chdir", "/opt/basil", "-c", "/opt/basil/gunicorn.py", "basil.wsgi:application"]