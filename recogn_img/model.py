from typing import Tuple, Any, Dict


class PredResult:
    PROB_MAX_DELTA_CONSIDERED_EQUAL = 0.1
    BOX_MAX_DELTA_CONSIDERED_EQUAL = 50

    __slots__ = ["obj_class", "prob", "box"]

    def __init__(self, obj_class: str, prob: float, box: Tuple[int, int, int, int]) -> None:
        self.obj_class = obj_class
        self.prob = prob  # in range [0.0 - 1.0]
        self.box = box  # top, left, width, height, all in pixels

    def __repr__(self):
        return f"{self.__class__.__name__}({self.obj_class}, {self.prob}, {self.box})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        prob_diff = abs(self.prob - other.prob)
        box_diff = [abs(self.box[i] - other.box[i]) for i in range(len(self.box))]
        return self.obj_class == other.obj_class \
               and prob_diff <= self.PROB_MAX_DELTA_CONSIDERED_EQUAL \
               and all([d <= self.BOX_MAX_DELTA_CONSIDERED_EQUAL for d in box_diff])

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.obj_class)

    def __lt__(self, other) -> bool:
        return self.__cmp__(other) == -1

    def __le__(self, other):
        r = self.__cmp__(other)
        return r == -1 or r == 0

    def __gt__(self, other):
        return self.__cmp__(other) == 1

    def __ge__(self, other):
        r = self.__cmp__(other)
        return r == 1 or r == 0

    def __cmp__(self, other):
        if self.obj_class == other.obj_class:
            if self.prob < other.prob:
                return -1
            elif self.prob > other.prob:
                return 1
            return 0
        else:
            if self.obj_class > other.obj_class:
                return 1
            else:
                return -1

    def to_serializable(self):
        return {"obj_class": self.obj_class, "prob": self.prob, "box": list(self.box)}

    @classmethod
    def from_serializable(cls, serial: Dict[str, Any]) -> 'PredResult':
        serial["box"] = tuple(serial["box"])
        return PredResult(**serial)
