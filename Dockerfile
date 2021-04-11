FROM ubuntu:20.10

RUN apt-get update -y && \
    apt-get install bash && \
    apt-get install -y python3-pip python3-dev && \
    apt-get install -y python3-pygame

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r requirements.txt

COPY . /

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]