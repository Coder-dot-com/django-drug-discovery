FROM python:3.10.12
ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get install -y python3-dev

WORKDIR /APP

COPY requirements.txt requirements.txt
COPY ./scripts /scripts
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /APP/REINVENT4

RUN pip3 install --no-deps . 

RUN reinvent --help

WORKDIR /APP/src

RUN adduser --disabled-password --no-create-home app


RUN mkdir -p /vol/web/static && \
    chown -R app:app /vol && \
    chmod -R 755 /vol

RUN chmod -R +x /scripts
WORKDIR /APP/src

ENV PATH="/scripts:/py/bin:$PATH"

# USER app #commented out for now

CMD ["run.sh"]