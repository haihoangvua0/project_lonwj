from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 50
import process_front_end as pfe
product_symbol = '\u00D7'
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
                else: return printing[:-1]
        @property
        def value(self):
                return pfe.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        
        # Data structure.
        def __repr__(self):
                return str(self)
        def __str__(self):
                printing = [self.x, self.y, self.z]
                if printing[-1] != 0:
                        return f"Vector({self.x},{self.y},{self.z})"
                else:
                        return f"Vector({self.x},{self.y})"
        
        # Math doing
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
                if isinstance(other, (int, float, Fraction, Decimal)):
                        if type(other) == int:
                                return Vector(
                                        self.x * other,
                                        self.y * other,
                                        self.z * other
                                )
                        elif isinstance(other, (float, Decimal)):
                                n = float(other)
                                if pfe.check_irrational(n):
                                        return Vector(
                                                self.x * n,
                                                self.y * n,
                                                self.z * n
                                        )
                                else:
                                        n = Fraction(*n.as_integer_ratio()).limit_denominator()
                                        if n.denominator == 1:
                                                return Vector(
                                                        self.x * n.numerator,
                                                        self.y * n.numerator,
                                                        self.z * n.numerator,
                                                )
                                        return Vector(
                                                self.x * n,
                                                self.y * n,
                                                self.z * n,
                                        )
                elif isinstance(other, Vector):
                        # Nhân vô hướng
                        return self.x * other.x + self.y * other.y + self.z * other.z
                
        def __rmul__(self, other): return self * other
        def __sub__(self, other):
            if not isinstance(other, Vector): return NotImplemented
            return self + (-1) * other
        def __rsub__(self, other):
            if not isinstance(other, Vector): return NotImplemented
            return (-1) * self + other
def product(*vec: Vector):
        def cross(a: Vector, b: Vector) -> Vector:
                ax, ay, az = a.x, a.y, a.z
                bx, by, bz = b.x, b.y, b.z
            
                return Vector(
                        ay * bz - az * by,
                        az * bx - ax * bz,
                        ax * by - ay * bx
                )
        if len(vec) < 2:
                raise ValueError("Cross product needs at least 2 vectors")
    
        result = vec[0]
        for v in vec[1:]:
                if not isinstance(v, Vector):
                       raise TypeError("All arguments must be Vector")
                result = cross(result, v)
    
        return result
def preprocess_vector(expr: str) -> str:
        import re
        import process_front_end as pfe

        expr = pfe.preprocess_expression(expr)

        CROSS = "\u00D7"
        vec = r'(VecA|VecB|VecC|VecD)'

        # ===== explicit cross: VecA×VecB =====
        pattern_explicit = re.compile(rf'({vec}){CROSS}({vec})')

        while pattern_explicit.search(expr):
            expr = pattern_explicit.sub(r'cross(\1,\2)', expr)

        # ===== implicit cross: VecA VecB =====
        pattern_implicit = re.compile(rf'({vec})\s+({vec})')

        while pattern_implicit.search(expr):
                expr = pattern_implicit.sub(r'product(\1,\2)', expr)

        return expr