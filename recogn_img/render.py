import json
from os import path
from typing import List, Any, Dict

import cv2
import numpy as np
import piexif

from recogn_img import PredResult
from recogn_img.utils import get_log


class RecognRender:
    def __init__(self, results_file_path: str, output_path: str, transfer_exif: bool) -> None:
        self.results_file_path = results_file_path
        self.output_path = output_path
        self.transfer_exif = transfer_exif
        self.log = get_log()

    def render(self) -> int:
        copied_images = 0
        with open(self.results_file_path, "r") as file_:
            all_results = json.load(file_)
        for img_file_path, results in all_results.items():
            if path.isfile(img_file_path):
                if results:
                    tgt_img_path = path.join(self.output_path, path.basename(img_file_path))
                    self._store_rendered_image(img_file_path, results, tgt_img_path)
                    copied_images += 1
            else:
                self.log.warning(f"Image {img_file_path} does not exist!")
        return copied_images

    def _store_rendered_image(self, orig_img_path: str, results: List[Dict[str, Any]], tgt_img_path: str) -> None:
        pred_results = [PredResult.from_serializable(r) for r in results]
        image = cv2.imread(orig_img_path)
        image = self._draw_boxes(image, results=pred_results)
        cv2.imwrite(tgt_img_path, image, [cv2.IMWRITE_JPEG_QUALITY, 40])
        if self.transfer_exif:
            self._transfer_exif(orig_img_path, tgt_img_path)

    def _draw_boxes(self, image: np.ndarray, results: List[PredResult]) -> np.ndarray:
        for result in results:
            x, y, w, h = result.box

            top = max(0, np.floor(x + 0.5).astype(int))
            left = max(0, np.floor(y + 0.5).astype(int))
            right = min(image.shape[1], np.floor(x + w + 0.5).astype(int))
            bottom = min(image.shape[0], np.floor(y + h + 0.5).astype(int))

            box_color_rgb = (255, 0, 0)
            cv2.rectangle(image, (top, left), (right, bottom), box_color_rgb, 2)

            text_fmt = '{0} {1:.2f}'.format(result.obj_class, result.prob)
            text_position = (top, left - 6)
            font_color_rgb = (0, 0, 255)
            font_scale, font_thickness = 0.6, 1
            cv2.putText(image, text_fmt, text_position, cv2.FONT_HERSHEY_SIMPLEX,
                        font_scale, font_color_rgb, font_thickness, cv2.LINE_AA)
        return image

    def _transfer_exif(self, src_img: str, tgt_img: str) -> None:
        original_exif = piexif.load(src_img)
        piexif.insert(piexif.dump(original_exif), tgt_img)
