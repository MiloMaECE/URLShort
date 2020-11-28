FROM python:3.6-stretch

ADD ./requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

WORKDIR /src

ENTRYPOINT ["python", "/src/app.py"]
