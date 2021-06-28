FROM amd64/python:slim

WORKDIR /code

COPY requirements.txt .

RUN pip install --proxy="$HTTP_PROXY" -r requirements.txt

COPY ./ ./src
WORKDIR /code/src

EXPOSE 5000
HEALTHCHECK --timeout=1s --interval=3600s CMD curl --fail --head --header "X-SOURCE: docker_healthcheck" localhost:5000/song

ENV API_DEBUG=${API_DEBUG:-False}
CMD [ "python", "shapes/app.py" ]
