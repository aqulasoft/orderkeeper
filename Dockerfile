FROM python:3.8

WORKDIR /code
COPY requirements.txt .

RUN pip install -U pip && pip install -r requirements.txt

COPY ./bot ./bot
CMD python -m bot
