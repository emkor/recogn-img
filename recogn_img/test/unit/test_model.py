from unittest import TestCase

from recogn_img import PredResult

RESULT_3 = PredResult("person", 0.65, (11, 12, 47, 80))
RESULT_2 = PredResult("bird", 0.54, (56, 64, 37, 121))
RESULT_1 = PredResult("person", 0.66, (10, 12, 46, 81))


class ModelTest(TestCase):
    def test_should_check_models_equality(self):
        self.assertNotEqual(RESULT_1, RESULT_2)
        self.assertEqual(RESULT_1, RESULT_3)

    def test_should_check_models_sorting(self):
        self.assertGreater(RESULT_1, RESULT_2)
        self.assertGreater(RESULT_1, RESULT_3)
        self.assertLess(RESULT_2, RESULT_3)
        self.assertLess(RESULT_3, RESULT_1)

    def test_should_repr_work_as_copy_paste(self):
        self.assertEqual(str(RESULT_1), 'PredResult(person, 0.66, (10, 12, 46, 81))')
