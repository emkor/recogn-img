# recogn-img [![Build Status](https://travis-ci.com/emkor/recogn-img.svg?branch=master)](https://travis-ci.com/emkor/recogn-img)
Library for simple object recognition on images using [YOLO model](https://pjreddie.com/darknet/yolo/).

Inspired by [machinelearningmastery.com](https://machinelearningmastery.com/how-to-perform-object-detection-with-yolov3-in-keras/) article by Jason Brownlee. 

## usage
- as a library:
```python
from recogn_img import read_classes, Recognizer

classes = read_classes("coco_classes.txt")
recognizer = Recognizer(model_path="yolov3.h5",  classes=classes,
                        img_width_height=(416, 416),
                        threshold_box_obj=(0.5, 0.6))
results = recognizer.recognize("my_image.jpg")
print(results)
```

- as CLI tool (single JSON with results):
```shell script
recogn-img yolov3.h5 coco_classes.txt ~/Pictures ~/RecognitionResults.json --img-width 416 --img-height 416 --box-threshold 0.5 --obj-threshold 0.6
```

- as CLI tool for storing images with rendered boxes in given dir:
```shell script
render-recogn ~/RecognitionResults.json ~/RenderedImgs/ --copy-exif
```

## prerequisites
- Linux with Python >= 3.7 installed
- CPU with AVX instruction extensions (`tensorflow>=1.5.1` requires them)
- YOLO pre-trained model (weights file) converted to Keras model (.h5 file), and file with list of classes for given model, both downloaded through `make dl_model` command for your convenience

## development
- for development, take a look at `Makefile`