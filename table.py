from typing import Callable
from process_front_end import *
def build_function(expr: str) -> Callable[[int | Fraction | float], int | Fraction | float]:
        def f(x: int | Fraction | float) -> int | Fraction | float:
                return evaluate_expression(expr.replace("x", f"({x})"))
        return f