from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 50
import process_front_end as pfe
class Vector:
        def __init__(self, 
                     x: int | Decimal | float | Fraction, 
                     y: int | Decimal | float | Fraction, 
                     z: int | Decimal | float | Fraction = 0):
                self.x = x
                self.y = y
                self.z = z
        
        # Property
        @property
        def items(self):
                printing = [self.x, self.y, self.z]
                if printing[-1] != 0:
                        return printing
                else: printing[:-1]

        def __repr__(self):
                return str(self)
        def __str__(self):
                printing = [self.x, self.y, self.z]
                if printing[-1] != 0:
                        return f"Vector({self.x},{self.y},{self.z})"
                else:
                        return f"Vector({self.x},{self.y})"
        def __add__(self, other):
                if not isinstance(other, Vector): return NotImplemented
                result = Vector(self.x + other.x,
                                self.y + other.y,
                                self.z + other.z
                )
                return result
        def __radd__(self, other):
                return self + other
        def __mul__(self, other):
                pass
