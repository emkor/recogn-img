import argparse
import json
from os import path
from typing import List

from recogn_img import PredResult
from recogn_img.recogn import Recognizer


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Detect objects on given image and output results')
    parser.add_argument('model_file', type=str, help='Path to Keras model (.h5 file)')
    parser.add_argument('classes_file', type=str,
                        help='File containing classes (each on new line) the model is predicting for')
    parser.add_argument('input_dir', type=str, help='Path do directory with images to analyze')
    parser.add_argument('results', type=str, default=None,
                        help='If set to directory, each result will be stored as JSON file named after source image; \
                        if set to non-existing file, results will be stored as single JSON file')
    parser.add_argument('--img-width', type=int, default=416,
                        help='Image width the given model is accepting (default: 416)')
    parser.add_argument('--img-height', type=int, default=416,
                        help='Image height the given model is accepting (default: 416)')
    parser.add_argument('--box-threshold', type=float, default=0.6, help='Box (nms) detection threshold')
    parser.add_argument('--obj-threshold', type=float, default=0.5, help='Object detection threshold')
    return parser.parse_args()


def read_classes(classes_file: str) -> List[str]:
    with open(classes_file) as f_:
        class_names = f_.readlines()
    return [c.strip() for c in class_names]


def main(model_file: str, classes_file: str, input_dir: str, results_path: str,
         obj_threshold: float, box_threshold: float, img_width: int, img_height: int) -> None:
    classes = read_classes(classes_file)
    recognizer = Recognizer(model_path=model_file, classes=classes,
                            img_width_height=(img_width, img_height),
                            threshold_box_obj=(box_threshold, obj_threshold))
    if path.exists(results_path) and path.isdir(results_path):
        print(
            f"Storing results under {path.abspath(results_path)} directory, one JSON file per image if image has objects in it.")
        for img_path, results in recognizer.recognize_all(input_dir):
            if results:
                target_json = "f{img_path}.json"
                with open(target_json, "w") as img_results_file:
                    json.dump(_serialized_results_desc(results), img_results_file)
    else:
        print(f"Storing results in single JSON file: {path.abspath(results_path)}")
        output = {}
        for img_path, results in recognizer.recognize_all(input_dir):
            if results:
                output.update({img_path: _serialized_results_desc(results)})
        if output:
            with open(results_path, "w") as results_file:
                json.dump(output, results_file)
        else:
            print("No detections, omitting creating results file!")
    print("Done!")


def _serialized_results_desc(results: List[PredResult]) -> List[PredResult]:
    return [r.to_serializable() for r in sorted(results, reverse=True)]


def cli_main() -> None:
    args = _parse_args()
    main(args.model_file, args.classes_file, args.input_dir, args.results, args.obj_threshold, args.box_threshold,
         args.img_width, args.img_height)


if __name__ == '__main__':
    main("/home/mat/proj/docker-img-obj-classification/keras_darknet_yolov3_2019_09_29.h5",
         "/home/mat/proj/docker-img-obj-classification/coco_classes.txt",
         "/home/mat/proj/recogn-img/tmp/input",
         "/home/mat/proj/recogn-img/tmp/results.json",
         0.6, 0.5, 416, 416)
