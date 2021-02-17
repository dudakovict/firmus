FROM python:3.9.1-slim

LABEL maintainer="dudakovict@gmail.com"

RUN apt-get update && \
    apt-get -y install netcat && \
    apt-get clean

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY ./Pipfile /usr/src/app/Pipfile
COPY ./Pipfile.lock /usr/src/app/Pipfile.lock

RUN pip install pipenv
RUN pipenv install --system --deploy

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

COPY . /usr/src/app

EXPOSE 5000

CMD ["/usr/src/app/entrypoint.sh"]