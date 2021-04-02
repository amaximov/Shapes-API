FROM python:latest

WORKDIR /code

COPY requirements.txt .

RUN pip install --proxy="$HTTP_PROXY" -r requirements.txt

COPY ./ ./src
WORKDIR /code/src

EXPOSE 5000
HEALTHCHECK --timeout=1s CMD curl --fail --head --header "X-SOURCE: docker_healthcheck" localhost:5000/song

CMD [ "python", "shapes/app.py" ]
