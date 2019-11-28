FROM python:3.7-slim-stretch

RUN apt update && apt install -y libsm6 libxext6 libxrender1

WORKDIR /src
RUN mkdir -p /image && mkdir -p /result && mkdir -p /render

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY yolov3.h5 .
COPY coco_classes.txt .

COPY dist/recogn_img-*.whl .
RUN pip install recogn_img-*.whl
