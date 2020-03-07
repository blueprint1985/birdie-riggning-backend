# Dockerfile - this is a comment. Delete me if you want.
FROM python:3.8.2
COPY ./src /usr/src
WORKDIR /usr/src
RUN apt-get install default-libmysqlclient-dev
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["run.py"]