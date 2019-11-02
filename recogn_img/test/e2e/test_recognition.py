from os import path
from unittest import TestCase

from recogn_img import Recognizer, read_classes
from recogn_img.test.utils import get_proj_file_path

TEST_IMG_RELATIVE_PATH = "recogn_img/test/resources/test_cctv_car_at_night.jpg"


class TestImgRecognition(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.classes_path = get_proj_file_path("coco_classes.txt")
        cls.model_path = get_proj_file_path("yolov3.h5")
        cls.recognizer = Recognizer(cls.model_path, read_classes(cls.classes_path), (416, 416))

    def setUp(self) -> None:
        self.assertTrue(path.isfile(self.classes_path))
        self.assertTrue(path.isfile(self.model_path))

    def test_should_recognize_car_on_night_cctv_image(self):
        # given
        test_img_path = get_proj_file_path(TEST_IMG_RELATIVE_PATH)
        self.assertTrue(path.isfile(test_img_path))

        # when
        results = self.recognizer.recognize(test_img_path)
        detected_classes = set([r.obj_class for r in results])

        # then
        self.assertGreaterEqual(len(results), 1)
        self.assertIn("car", detected_classes)
