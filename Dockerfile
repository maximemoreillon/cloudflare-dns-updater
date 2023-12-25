FROM python:3.10

WORKDIR /usr/src/app

COPY . .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt


CMD python main.py
