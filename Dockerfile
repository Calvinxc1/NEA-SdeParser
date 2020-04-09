FROM python:3-slim

COPY ./nea_sdeParser /srv/app/nea_sdeParser
WORKDIR /srv/app
COPY ./setup.py ./
RUN python -m pip install ./ \
    && rm -rf ./nea_sdeParser

COPY ./app.py ./

VOLUME /srv/app/config.py
VOLUME /srv/app/gunicorn.py

CMD ["gunicorn", "-c", "./gunicorn.py", "app:app"]