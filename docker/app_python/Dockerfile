FROM python:3.8.6-slim-buster
MAINTAINER "Boon SUI <boonsuli@gmail.com>"
WORKDIR /app_python

# copy the dependencies file
COPY ./docker/app_python/requirements.txt /app_python/requirements.txt

# install dependencies
RUN pip install -r /app_python/requirements.txt

# copy the content of the local src directory
COPY ./app_python /app_python

# set env variable
ENV FLASK_ENV = "docker"

# run server
ENTRYPOINT ["python"]
CMD [ "/app_python/UserModule.py" ]
