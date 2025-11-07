# casio_core.py
# Backend module for FX-580 simulator (functions collected & refined)
import math
from decimal import Decimal, getcontext

MATH_ERROR = "MATH ERROR"
pi, e = math.pi, math.e

getcontext().prec = 12

# 1. Physical Constants
constants = {
    "General": {
        "c": 2.99792458e8,
        "g": 9.80665,
        "h": 6.62607015e-34,
        "G": 6.67430e-11,
        "Na": 6.02214076e23,
        "k": 1.380649e-23,
        "R": 8.314462618,
        "eV": 1.602176634e-19,
    },
    "Electromagnetic": {
        "e": 1.602176634e-19,
        "mu_0": 1.25663706212e-6,
        "eps_0": 8.8541878128e-12,
        "KJ": 4.835978484e14,
        "RK": 25812.80745,
    },
    "Atomic_Nuclear": {
        "m_e": 9.1093837015e-31,
        "m_p": 1.67262192369e-27,
        "m_n": 1.67492749804e-27,
        "e_over_me": 1.75882001076e11,
        "u": 1.66053906660e-27,
    },
    "Phys_Chem": {
        "atm": 1.01325e5,
        "Vm": 22.41396954,
        "F": 96485.33212,
    },
    "Adopted": {
        "cal": 4.184,
        "eV": 1.602176634e-19,
        "mmHg": 133.322368,
        "inch": 0.0254,
        "lb": 0.45359237,
    },
    "Others": {
        "phi": (1 + 5 ** 0.5) / 2,
        "pi": math.pi,
        "deg_to_rad": math.pi / 180,
        "rad_to_deg": 180 / math.pi,
    }
}

def get_constant(name: str):
    for group in constants.values():
        if name in group:
            return group[name]
    raise KeyError(MATH_ERROR)

# 2. Angle mode (global)
ANGLE_MODE = "DEG"

def set_angle_mode(mode: str):
    global ANGLE_MODE
    mode = mode.strip().upper()
    if mode not in ("DEG", "RAD", "GRA"):
        raise ValueError(MATH_ERROR)
    ANGLE_MODE = mode

def _to_radian_if_needed(x: float):
    if ANGLE_MODE == "DEG":
        return math.radians(x)
    if ANGLE_MODE == "GRA":
        return x * math.pi / 200
    return x

# 3. Trig functions (Casio-compatible)
def sin(x: float): return math.sin(_to_radian_if_needed(x))
def cos(x: float): return math.cos(_to_radian_if_needed(x))
def tan(x: float):
    a = _to_radian_if_needed(x)
    if math.isclose(math.cos(a), 0, abs_tol=1e-12):
        return float("inf")
    return math.tan(a)
def asin(x: float):
    v = math.asin(x)
    return math.degrees(v) if ANGLE_MODE == "DEG" else v
def acos(x: float):
    v = math.acos(x)
    return math.degrees(v) if ANGLE_MODE == "DEG" else v
def atan(x: float):
    v = math.atan(x)
    return math.degrees(v) if ANGLE_MODE == "DEG" else v

# 4. Core helpers
def sqrt_simplify(n: int):
    if n < 0:
        return (1, n)
    a, b = 1, n
    i = 2
    while i * i <= b:
        while b % (i * i) == 0:
            b //= i * i
            a *= i
        i += 1
    return (a, b)

def check_irrational(n: float) -> bool:
    try:
        from fractions import Fraction
        f = Fraction(n).limit_denominator()
        return abs(float(f) - n) > 1e-100
    except Exception:
        return True

# 5. Unified returning()
def returning(n: int | float | Decimal, choice: str = "D"):
    if isinstance(n, Decimal):
        n = float(n)
    if isinstance(n, int):
        return n
    if math.isnan(n) or math.isinf(n):
        return str(n)
    if abs(n - round(n)) < 1e-10:
        return int(round(n))
    if choice.upper() == "S":
        if check_irrational(n):
            k = round(n * n)
            if abs(k - n * n) < 1e-9 and k < 1e6:
                a, b = sqrt_simplify(k)
                if b == 1: return str(a)
                if a == 1: return f"sqrt({b})"
                return f"{a}sqrt({b})"
            return f"{n:.10f}".rstrip("0").rstrip(".")
        from fractions import Fraction
        f = Fraction(n).limit_denominator()
        if f.denominator == 1:
            return str(f.numerator)
        return f"{f.numerator}/{f.denominator}"
    if abs(n) >= 1e10 or (0 < abs(n) < 1e-6):
        return f"{n:.8e}"
    return f"{n:.10f}".rstrip("0").rstrip(".")

# 6. Expression engine
def preprocess_expression(expr: str) -> str:
    import re
    expr = re.sub(r'\s+', '', expr)
    expr = re.sub(r'(\d)([A-Za-z\(])', r'\1*\2', expr)
    expr = re.sub(r'([A-Za-z0-9\)])\(', r'\1*(', expr)
    expr = re.sub(r'\)([A-Za-z0-9])', r')*\1', expr)
    return expr

def evaluate_expression(expr: str, simplify_symbolic=True):
    expr_clean = preprocess_expression(expr)
    try:
        import sympy as sp
        HAS_SYMPY = True
    except Exception:
        HAS_SYMPY = False
    if HAS_SYMPY:
        try:
            s = sp.sympify(expr_clean, evaluate=True)
            if simplify_symbolic:
                return sp.simplify(sp.radsimp(s))
            return s
        except Exception:
            pass
    try:
        safe = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        safe.update({"pi": pi, "e": e})
        return eval(expr_clean, {"__builtins__": {}}, safe)
    except Exception:
        return MATH_ERROR

def calc(expr: str):
    try:
        import sympy as sp
        HAS_SYMPY = True
    except Exception:
        HAS_SYMPY = False
    r = evaluate_expression(expr, simplify_symbolic=False)
    if HAS_SYMPY:
        if 'sp' not in locals():
            import sympy as sp
        if isinstance(r, sp.Expr):
            try:
                return r.evalf()
            except Exception:
                return str(r)
    return r

def solve_eq(expression: str):
    from sympy import Eq, symbols, solve as s_solve, sympify
    x = symbols("x")
    if "=" in expression:
        left, right = expression.split("=")
        eq = Eq(sympify(left), sympify(right))
    else:
        eq = Eq(sympify(expression), 0)
    return s_solve(eq, x)

# 7. Roots
def fact(n: int):
    if n < 2:
        return []
    f, i = [], 2
    while i * i <= n:
        c = 0
        while n % i == 0:
            n //= i
            c += 1
        if c > 0:
            f.append((i, c))
        i += 1
    if n > 1:
        f.append((n, 1))
    return f

def sqrt(n: int | float):
    if n < 0: return MATH_ERROR
    return returning(math.sqrt(n), "S")

def nth_root(base: int | float, ex: int):
    if not isinstance(ex, int) or ex == 0:
        raise ValueError(MATH_ERROR)
    if base < 0:
        if ex % 2 == 0:
            return MATH_ERROR
        result = -float(pow(abs(base), 1 / abs(ex)))
    else:
        result = float(pow(base, 1 / abs(ex)))
    if ex < 0:
        if result == 0: return MATH_ERROR
        result = 1 / result
    return returning(result)

# 8. Differentials + log
def log(base: float, num: float):
    if base <= 0 or base == 1:
        raise ValueError("Cơ số phải > 0 và != 1")
    if num <= 0:
        raise ValueError("Số cần lấy log phải > 0")
    return returning(math.log(num, base))

def ln(num: float):
    if num <= 0:
        raise ValueError("Số cần lấy ln phải > 0")
    return returning(log(math.e, num))

def d_dy(expression: str, var: str = "x"):
    from sympy import symbols, diff, sympify
    x = symbols(var)
    expr = sympify(expression)
    return diff(expr, x)

def integral(low: float, high: float, expression: str, var: str = "x"):
    from sympy import symbols, integrate, sympify
    x = symbols(var)
    expr = sympify(expression)
    return returning(integrate(expr, (x, low, high)))

# 9. Tổng / Tích liên tục
def sigma(first: int, end: int, expression: str, var: str = "i"):
    from sympy import symbols, summation, sympify
    i = symbols(var)
    expr = sympify(expression)
    return returning(summation(expr, (i, first, end)))

def continuous_mul(first: int, end: int, expression: str, var: str = "i"):
    from sympy import symbols, product, sympify
    i = symbols(var)
    expr = sympify(expression)
    return returning(product(expr, (i, first, end)))

# Debug time.
if __name__ == "__main__":
    print("=== Debug: get_constant ===")
    for group in constants:
        for key in constants[group]:
            try:
                print(f"{key}: {get_constant(key)}")
            except Exception as e:
                print(f"Error with {key}: {e}")

    print("\n=== Debug: set_angle_mode & trig functions ===")
    for mode in ["DEG", "RAD", "GRA"]:
        set_angle_mode(mode)
        print(f"\nAngle mode: {mode}")
        for val in [0, 30, 45, 60, 90, 180]:
            print(f"sin({val}) = {sin(val)}")
            print(f"cos({val}) = {cos(val)}")
            print(f"tan({val}) = {tan(val)}")
        for val in [0, 0.5, 1]:
            print(f"asin({val}) = {asin(val)}")
            print(f"acos({val}) = {acos(val)}")
            print(f"atan({val}) = {atan(val)}")

    print("\n=== Debug: sqrt_simplify ===")
    for n in [4, 8, 12, 18, 20, 50, 72, 100]:
        print(f"sqrt_simplify({n}) = {sqrt_simplify(n)}")

    print("\n=== Debug: check_irrational ===")
    for n in [0.5, 1/3, math.sqrt(2), math.pi]:
        print(f"check_irrational({n}) = {check_irrational(n)}")

    print("\n=== Debug: returning ===")
    for n in [2, 2.0, 2.0000000001, 1/3, math.sqrt(2), 1e12, 1e-8]:
        for choice in ["D", "S"]:
            print(f"returning({n}, '{choice}') = {returning(n, choice)}")

    print("\n=== Debug: preprocess_expression ===")
    for expr in ["2sin(30)", "3(x+1)", "(x+1)2", "2(x+1)3"]:
        print(f"preprocess_expression('{expr}') = {preprocess_expression(expr)}")

    print("\n=== Debug: evaluate_expression ===")
    for expr in ["2+2", "sin(pi/2)", "sqrt(2)", "x+1"]:
        print(f"evaluate_expression('{expr}') = {evaluate_expression(expr)}")

    print("\n=== Debug: calc ===")
    for expr in ["2+2", "sin(pi/2)", "sqrt(2)", "x+1"]:
        print(f"calc('{expr}') = {calc(expr)}")

    print("\n=== Debug: solve_eq ===")
    for expr in ["x+2=5", "x**2-4=0", "x**2+x+1=0"]:
        print(f"solve_eq('{expr}') = {solve_eq(expr)}")

    print("\n=== Debug: fact ===")
    for n in [12, 60, 97, 100]:
        print(f"fact({n}) = {fact(n)}")

    print("\n=== Debug: sqrt ===")
    for n in [4, 2, 9, 50, -1]:
        print(f"sqrt({n}) = {sqrt(n)}")

    print("\n=== Debug: nth_root ===")
    for base, ex in [(8, 3), (16, 4), (-8, 3), (16, -2), (0, 2)]:
        try:
            print(f"nth_root({base}, {ex}) = {nth_root(base, ex)}")
        except Exception as e:
            print(f"nth_root({base}, {ex}) error: {e}")

    print("\n=== Debug: log & ln ===")
    for base, num in [(10, 100), (2, 8), (math.e, math.e**2), (1, 10), (10, -1)]:
        try:
            print(f"log({base}, {num}) = {log(base, num)}")
        except Exception as e:
            print(f"log({base}, {num}) error: {e}")
    for num in [math.e, 10, -1]:
        try:
            print(f"ln({num}) = {ln(num)}")
        except Exception as e:
            print(f"ln({num}) error: {e}")

    print("\n=== Debug: d_dy ===")
    for expr in ["x**2", "sin(x)", "exp(x)", "x**3+2*x"]:
        print(f"d_dy('{expr}') = {d_dy(expr)}")

    print("\n=== Debug: integral ===")
    for expr in ["x", "x**2", "sin(x)"]:
        print(f"integral(0, 1, '{expr}') = {integral(0, 1, expr)}")

    print("\n=== Debug: sigma ===")
    for expr in ["i", "i**2"]:
        print(f"sigma(1, 5, '{expr}') = {sigma(1, 5, expr)}")

    print("\n=== Debug: continuous_mul ===")
    for expr in ["i", "i+1"]:
        print(f"continuous_mul(1, 4, '{expr}') = {continuous_mul(1, 4, expr)}")
