FROM python:3-slim

ARG schema_branch=develop

RUN apt-get update \
    && apt-get install -y git \
    && python -m pip install --upgrade pip

WORKDIR /srv/app

COPY ./ ./NEA-SdeParser/
RUN git clone -b $schema_branch https://github.com/Calvinxc1/NEA-Schema.git \
    && python -m pip install --no-cache-dir ./NEA-Schema \
    && python -m pip install --no-cache-dir ./NEA-SdeParser \
    && rm -rf ./NEA-Schema \
    && rm -rf ./NEA-SdeParser

VOLUME /srv/app/config.py
VOLUME /srv/app/gunicorn.py

CMD ["gunicorn", "-c", "./gunicorn.py", "nea_sdeParser:app"]