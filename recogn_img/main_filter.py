import argparse
import os
from datetime import date, time, datetime
from typing import Set, Any, Dict, Tuple, List

from recogn_img import PredResult
from recogn_img.utils import setup_log, get_log, read_json, write_json


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Filters results based on class whitelist and movement per cam')
    parser.add_argument('input', type=str, help='Results file to be apply filtering on')
    parser.add_argument('output', type=str, help='Where to store filtered results')
    parser.add_argument('--whitelist', type=str, default=None,
                        help='Comma-separated list of object classes to pass through filter')
    parser.add_argument('--verbose', action='store_true', help='Enable more verbose logging')
    return parser.parse_args()


def filter_classes(input_content: Dict[str, Any], whitelist: Set[str]) -> Dict[str, Any]:
    output = {}
    for img_path, detections in input_content.items():
        detections = [d for d in detections if d["obj_class"] in whitelist]
        if detections:
            output[img_path] = detections
    print(f"After filtering: {len(output)}/{len(input_content)} images")
    return output


def parse_file_name(file_path: str) -> Tuple[str, datetime]:
    file_name_parts = os.path.basename(file_path).split("_")
    img_dt = datetime.combine(date.fromisoformat(file_name_parts[0]),
                              time.fromisoformat(file_name_parts[1].replace("-", ":")))
    cam_name = f"{file_name_parts[2]}_{file_name_parts[3]}"
    return cam_name, img_dt


def has_movement(pred_results_1: List[PredResult], pred_results_2: List[PredResult]) -> bool:
    if len(pred_results_1) != len(pred_results_2):
        return True
    pred_results_1 = sorted(pred_results_1)
    pred_results_2 = sorted(pred_results_2)
    for (pr1, pr2) in zip(pred_results_1, pred_results_2):
        if pr1 != pr2:
            return True
    return False


LAST_IMG_PER_CAM: Dict[str, str] = {}


def main(input_file: str, output_file: str, whitelist: Set[str]) -> None:
    setup_log()
    log = get_log()

    content = read_json(input_file)
    log.info(f"Read file {input_file} containing {len(content)} images, filtering...")

    if whitelist:
        content = filter_classes(content, whitelist)

    log.info("De-serializing prediction result objects...")
    for img_path, pred_results_dict_list in content.items():
        content.update({img_path: [PredResult.from_serializable(pr) for pr in pred_results_dict_list]})

    log.info(f"Checking for movement between photos...")
    output: Dict[str, List[PredResult]] = {}
    sorted_img_paths = sorted([img_path for img_path in content.keys()])
    for img_path in sorted_img_paths:
        cam, dt = parse_file_name(img_path)
        if cam in LAST_IMG_PER_CAM:
            if has_movement(content[LAST_IMG_PER_CAM[cam]], content[img_path]):
                output[img_path] = content[img_path]
        else:
            output[img_path] = content[img_path]
        LAST_IMG_PER_CAM[cam] = img_path

    serialized: Dict[str, List[Dict[str, Any]]] = {img_path: [p.to_serializable() for p in preds]
                                                   for img_path, preds in output.items()}
    log.info(f"Writing {len(serialized)} images data to {output_file}")
    write_json(serialized, output_file)


def cli_main():
    args = _parse_args()
    if args.input == args.output:
        raise ValueError("Can not use same file as input and output")
    if not os.path.isfile(args.input):
        raise ValueError(f"Input file {args.input} is not a file")
    whitelist_classes = set([c.strip() for c in args.whitelist.split(",") if c.strip()] if args.whitelist else [])

    main(args.input, args.output, whitelist_classes)


if __name__ == '__main__':
    cli_main()
