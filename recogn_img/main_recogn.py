import argparse
import json
import time
from os import path
from typing import List, Dict, Any

from recogn_img import PredResult
from recogn_img.recogn import Recognizer
from recogn_img.utils import setup_log, get_log, read_classes


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Detect objects on given image and output results')
    parser.add_argument('model_file', type=str, help='Path to Keras model (.h5 file)')
    parser.add_argument('classes_file', type=str,
                        help='File containing classes (each on new line) the model is predicting for')
    parser.add_argument('input_dir', type=str, help='Path do directory with images to analyze')
    parser.add_argument('results_file', type=str, default=None, help='Results will be stored as single JSON file')
    parser.add_argument('--img-width', type=int, default=416,
                        help='Image width the given model is accepting (default: 416)')
    parser.add_argument('--img-height', type=int, default=416,
                        help='Image height the given model is accepting (default: 416)')
    parser.add_argument('--box-threshold', type=float, default=0.6, help='Box (nms) detection threshold')
    parser.add_argument('--obj-threshold', type=float, default=0.5, help='Object detection threshold')
    parser.add_argument('--verbose', action='store_true', help='Enable more verbose logging')
    return parser.parse_args()


def main(model_file: str, classes_file: str, input_dir: str, results_path: str,
         obj_threshold: float, box_threshold: float, img_width: int, img_height: int, verbose: bool) -> None:
    setup_log(verbose=verbose)
    log = get_log()
    classes = read_classes(classes_file)
    recognizer = Recognizer(model_path=model_file, classes=classes,
                            img_width_height=(img_width, img_height),
                            threshold_box_obj=(box_threshold, obj_threshold))
    start_time, output, detections, images = time.time(), {}, 0, 0
    for img_path, results in recognizer.recognize_all(input_dir):
        images += 1
        if results:
            detections += 1
            output.update({img_path: _serialized_results_desc(results)})
            log.debug(f"Detection on {path.basename(img_path)}: {set([r.obj_class for r in results])}")
    if output:
        with open(results_path, "w") as results_file:
            json.dump(output, results_file)
    else:
        log.info("No detections, omitting creating results file")
    took_sec = time.time() - start_time
    log.info(
        f"Done. Detection count: {detections}/{images} ({(detections / images * 100):.2f}%), \
        took {took_sec:.1f}s = {(took_sec / images):.3f}s/image")


def _serialized_results_desc(results: List[PredResult]) -> List[Dict[str, Any]]:
    return [r.to_serializable() for r in sorted(results, reverse=True)]


def cli_main() -> None:
    args = _parse_args()
    main(args.model_file, args.classes_file, args.input_dir, args.results, args.obj_threshold, args.box_threshold,
         args.img_width, args.img_height, args.verbose)


if __name__ == '__main__':
    cli_main()
