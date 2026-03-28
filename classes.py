import math

import numpy as np


class TFN:

    def __init__(self, a, b, c):
        #np.asarray(a).item()

        self.a = a
        self.b = b
        self.c = c

    def __repr__(self):
        return f"({self.a}, {self.b}, {self.c})"

    def __mul__(self, other):
        return TFN(
            self.a * other.a,
            self.b * other.b,
            self.c * other.c
        )


def scalar_product(A:TFN, num):
    return TFN(A.a * num, A.b * num, A.c * num)

def fuzzy_distance(A: TFN, B: TFN) -> float:
    return math.sqrt(
        ((A.a - B.a)**2 +
         (A.b - B.b)**2 +
         (A.c - B.c)**2) / 3.0
    )


class Selector:
    def __init__(self, vet_min, vet_max):
        self.vet_min = vet_min
        self.vet_max = vet_max

    def set_bounds(self,new_min,new_max):
        self.vet_min = new_min
        self.vet_max = new_max