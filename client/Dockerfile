from python:alpine3.6
#ref: https://hub.docker.com/_/python/
RUN apk update
RUN apk add gcc
RUN apk add python-dev
RUN apk add python3-dev
RUN apk add musl-dev
RUN apk add libffi
RUN apk add libffi-dev
RUN apk add openssl
RUN apk add openssl-dev
#RUN apk add libpython3-dev
#RUN apk add libpython3.4-dev
#RUN apk add libpython3.5-dev 
#RUN apk add python-numpy

WORKDIR /usr/source/app

COPY * ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "/usr/source/app/run.py" ]