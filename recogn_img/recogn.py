import os
from copy import copy
from typing import List, Tuple, Optional, Generator

import cv2
import numpy as np

from recogn_img.model import PredResult
from recogn_img.utils import get_log
from recogn_img.yolo import YoloModel

DEFAULT_BOX_THRESHOLD = 0.5
DEFAULT_OBJECT_THRESHOLD = 0.6


class Recognizer:
    def __init__(self, model_path: str, classes: List[str], img_width_height: Tuple[int, int],
                 threshold_box_obj: Tuple[float, float] = (DEFAULT_BOX_THRESHOLD, DEFAULT_OBJECT_THRESHOLD)) -> None:
        self.model_path = model_path
        self.classes = classes
        self.img_width_height = img_width_height
        self.threshold_box_obj = threshold_box_obj
        self._yolo_model: Optional[YoloModel] = None
        self.log = get_log()

    def recognize(self, img_path: str) -> List[PredResult]:
        image = cv2.imread(img_path)
        orig_shape_height_width = copy(image.shape)[0], copy(image.shape)[1]
        img_np_array = self._pre_process_image(image)
        return self._detect_image(img_np_array, self._get_model(), orig_shape_height_width)

    def recognize_all(self, dir_path: str) -> Generator[Tuple[str, List[PredResult]], None, None]:
        file_paths = [os.path.join(dir_path, p) for p in os.listdir(dir_path)]
        for file_path in [p for p in file_paths if os.path.isfile(p)]:
            try:
                yield (file_path, self.recognize(file_path))
            except Exception as e:
                self.log.warning(f"Could not analyze {file_path}: {e}")

    def _get_model(self) -> YoloModel:
        if self._yolo_model is None:
            self._yolo_model = YoloModel(keras_model=self.model_path,
                                         obj_threshold=self.threshold_box_obj[1],
                                         nms_threshold=self.threshold_box_obj[0])
        return self._yolo_model

    def _pre_process_image(self, img: np.ndarray) -> np.ndarray:
        image = cv2.resize(img, (self.img_width_height[1], self.img_width_height[0]), interpolation=cv2.INTER_CUBIC)
        image = np.array(image, dtype='float32')
        image /= 255.
        return np.expand_dims(image, axis=0)

    def _detect_image(self, image: np.ndarray, model: YoloModel,
                      orig_img_height_width: Tuple[int, int]) -> List[PredResult]:
        boxes, classes, scores = model.predict(image, orig_img_height_width)
        results = []
        if scores is not None:
            for box, class_, score in zip(boxes, classes, scores):
                result = PredResult(obj_class=str(self.classes[class_]),
                                    box=tuple([int(i) for i in box])[:4],
                                    prob=float(score))
                results.append(result)
        return results
