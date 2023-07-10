FROM python:3.10

COPY . /aiapi
WORKDIR /aiapi

RUN pip install -r requirements.txt

CMD ["python", "manage.py"]

