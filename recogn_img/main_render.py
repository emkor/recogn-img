import argparse
import time
from os import path
from typing import List

from recogn_img import PredResult
from recogn_img.render import RecognRender
from recogn_img.utils import setup_log, get_log


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Render stored results as boxes and store as new image')
    parser.add_argument('results_file', type=str, help='Path to stored results JSON file')
    parser.add_argument('output_dir', type=str,
                        help='Path do directory where images with rendered boxes should be stored')
    parser.add_argument('--copy-exif', action='store_true', help='Transfer EXIF data to images with rendered boxes')
    parser.add_argument('--verbose', action='store_true', help='Enable more verbose logging')
    return parser.parse_args()


def main(results_file: str, output_dir: str, copy_exif: bool, verbose: bool) -> None:
    setup_log(verbose=verbose)
    log = get_log()
    start_time = time.time()
    copied_images = 0
    renderer = RecognRender(results_file_path=results_file, output_path=output_dir, transfer_exif=copy_exif)
    if path.exists(results_file) and path.isdir(output_dir):
        copied_images = renderer.render()
    else:
        log.error(f"Either given results file {results_file} or output path {output_dir} does not exist")
        exit(1)
    took_sec = time.time() - start_time
    log.info(f"Done, took {took_sec:.1f}s = {(took_sec / copied_images):.3f}s/image")


def _serialized_results_desc(results: List[PredResult]) -> List[PredResult]:
    return [r.to_serializable() for r in sorted(results, reverse=True)]


def cli_main() -> None:
    args = _parse_args()
    main(args.results_file, args.output_dir, args.copy_exif, args.verbose)


if __name__ == '__main__':
    cli_main()
