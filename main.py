import math
import sys


def solve(a: float, b: float, c: float) -> list[float]:
    if abs(a) < sys.float_info.epsilon:
        raise Exception("Null 'a' argument")
    if not math.isfinite(a) or not math.isfinite(b) or not math.isfinite(c):
        raise Exception("Incorrect argument")
    d = b * b - 4 * a * c
    if d > 0:
        return [(-b + math.sqrt(d)) / (2 * a), (-b - math.sqrt(d)) / (2 * a)]
    if d < 0:
        return []
    if abs(d) < sys.float_info.epsilon:
        return [-b / (2 * a), -b / (2 * a)]