from typing import Tuple, Any, Dict


class PredResult:
    PROB_MAX_DELTA_CONSIDERED_EQUAL = 0.1
    BOX_MAX_DELTA_CONSIDERED_EQUAL = 4

    __slots__ = ["obj_class", "prob", "box"]

    def __init__(self, obj_class: str, box: Tuple[int, int, int, int], prob: float) -> None:
        self.obj_class = obj_class
        self.box = box  # top, left, width, height, all in pixels
        self.prob = prob  # in range [0.0 - 1.0]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.obj_class}, {self.prob}, {self.box})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.obj_class == other.obj_type \
               and abs(self.prob - other.prob) <= self.PROB_MAX_DELTA_CONSIDERED_EQUAL \
               and all([abs(self.box[i] - other.box[1]) <= self.BOX_MAX_DELTA_CONSIDERED_EQUAL
                        for i in range(len(self.box))])

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.obj_class)

    def __cmp__(self, other):
        if self.prob < other.prob:
            return -1
        elif self.prob > other.prob:
            return 1
        return 0

    def to_serializable(self):
        return {"obj_class": self.obj_class, "prob": self.prob, "box": list(self.box)}

    @classmethod
    def from_serializable(cls, serial: Dict[str, Any]) -> 'PredResult':
        serial["box"] = tuple(serial["box"])
        return PredResult(**serial)
