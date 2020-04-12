ARG BRANCH=develop

FROM python:3-slim

RUN apt-get update \
    && apt-get install -y git \
    && python -m pip install --upgrade pip

WORKDIR /srv/app

RUN git clone -b develop https://github.com/Calvinxc1/NEA-Schema.git \
    && git clone -b ${BRANCH} https://github.com/Calvinxc1/NEA-SdeParser.git \
    && python -m pip install --no-cache-dir ./NEA-Schema \
    && python -m pip install --no-cache-dir ./NEA-SdeParser \
    && rm -rf ./NEA-Schema \
    && rm -rf ./NEA-SdeParser

VOLUME /srv/app/config.py
VOLUME /srv/app/gunicorn.py

CMD ["gunicorn", "-c", "./gunicorn.py", "nea_sdeParser:app"]