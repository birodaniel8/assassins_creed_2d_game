FROM python:3.8-slim-buster

RUN pip install pipenv

COPY ./Pipfile /Pipfile

COPY ./Pipfile.lock /Pipfile.lock

WORKDIR /

RUN pipenv install

RUN pipenv lock --keep-outdated --requirements > requirements.txt

RUN pip install -r requirements.txt

COPY . /

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]