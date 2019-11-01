# recogn-img
Library for simple object recognition on images using YOLO model

## usage
- as library:
```python
from recogn_img import read_classes, Recognizer

classes = read_classes("coco_classes.txt")
recognizer = Recognizer(model_path="yolov3.h5",  classes=classes,
                        img_width_height=(416, 416),
                        threshold_box_obj=(0.5, 0.6))
results = recognizer.recognize("my_image.jpg")
print(results)
```

- as CLI tool (each image results in separate JSON file, if `~/RecognitionResults` is directory):
```shell script
recogn-img yolov3.h5 coco_classes.txt ~/Pictures ~/RecognitionResults --img-width 416 --img-height 416 --box-threshold 0.5 --obj-threshold 0.6
```

- as CLI tool (single JSON with results):
```shell script
recogn-img yolov3.h5 coco_classes.txt ~/Pictures ~/RecognitionResults.json --img-width 416 --img-height 416 --box-threshold 0.5 --obj-threshold 0.6
```

## prerequisites
- Linux with Python >=3.6 installed
- CPU with AVX instruction extensions (`tensorflow>=1.5.1` requires them)
- YOLO pre-trained model (weights file) converted to Keras model, available [in this B2 bucket](https://f001.backblazeb2.com/file/ml-model/keras_darknet_yolov3_2019_09_29.h5.zip)
- file with list of classes for given model, available [in this B2 bucket](https://f001.backblazeb2.com/file/ml-model/keras_darknet_yolov3_2019_09_29_coco_classes.txt)

### running tests
- install test tools with `pip install -r requirements-dev.txt`
- unit tests: `pytest -v --cov=./recogn_img ./recogn_img/test`
- type check: `mypy --ignore-missing-imports ./recogn_img`