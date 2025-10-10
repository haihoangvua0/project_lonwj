# ============================================
# Casio FX-580 Simulator Core (Backend Module)
# ============================================
from math import *
from decimal import Decimal, getcontext

getcontext().prec = 12  # độ chính xác toàn cục

# =============================
# Utility: Chuẩn hóa kết quả
# =============================
def returning(n: int | float | Decimal):
    """Chuẩn hóa kết quả số học trước khi hiển thị ra màn hình."""
    if isinstance(n, Decimal):
        n = float(n)

    if abs(n - round(n)) < 1e-9:
        return int(round(n))

    if abs(n) >= 1e10 or (0 < abs(n) < 1e-6):
        return f"{n:.8e}"

    s = f"{n:.10f}".rstrip("0").rstrip(".")
    return s


# =============================
# Góc: Độ / Radian / Grad
# =============================
ANGLE_MODE = "DEG"

def change_degree(choice: str):
    """Chọn chế độ góc toàn cục: DEG, RAD, GRA."""
    global ANGLE_MODE
    choice = choice.upper()
    if choice not in ("DEG", "RAD", "GRA"):
        raise ValueError("Chọn 'DEG', 'RAD' hoặc 'GRA'")
    ANGLE_MODE = choice
    return f"Chế độ góc: {ANGLE_MODE}"

def _to_radian(angle: float):
    """Chuyển góc sang radian theo ANGLE_MODE."""
    if ANGLE_MODE == "DEG":
        return radians(angle)
    elif ANGLE_MODE == "GRA":
        return angle * pi / 200
    return angle


# =============================
# Lượng giác
# =============================
def sin_(x: float): return returning(sin(_to_radian(x)))
def cos_(x: float): return returning(cos(_to_radian(x)))
def tan_(x: float): return returning(tan(_to_radian(x)))

def asin_(x: float): return returning(degrees(asin(x)) if ANGLE_MODE == "DEG" else asin(x))
def acos_(x: float): return returning(degrees(acos(x)) if ANGLE_MODE == "DEG" else acos(x))
def atan_(x: float): return returning(degrees(atan(x)) if ANGLE_MODE == "DEG" else atan(x))

def sinh_(x: float): return returning(sinh(x))
def cosh_(x: float): return returning(cosh(x))
def tanh_(x: float): return returning(tanh(x))

def asinh_(x: float): return returning(asinh(x))
def acosh_(x: float): return returning(acosh(x))
def atanh_(x: float): return returning(atanh(x))


# =============================
# Phép tính vi phân / tích phân
# =============================
def d_dy(expression: str, var: str = "x"):
    """Tính đạo hàm biểu thức (dùng sympy)."""
    from sympy import symbols, diff, sympify
    x = symbols(var)
    expr = sympify(expression)
    return returning(diff(expr, x))

def integral(low: float, high: float, expression: str, var: str = "x"):
    """Tính tích phân xác định."""
    from sympy import symbols, integrate, sympify
    x = symbols(var)
    expr = sympify(expression)
    return returning(integrate(expr, (x, low, high)))


# =============================
# Giải và tính toán biểu thức
# =============================
def solve_eq(expression: str):
    """Giải phương trình: sin(x)=0, 2x+1=0,..."""
    from sympy import Eq, symbols, solve as s_solve, sympify
    x = symbols("x")
    if "=" in expression:
        left, right = expression.split("=")
        eq = Eq(sympify(left), sympify(right))
    else:
        eq = Eq(sympify(expression), 0)
    return s_solve(eq, x)

def calc(expression: str):
    """Tính giá trị biểu thức toán học (safe eval)."""
    try:
        safe_dict = {k: v for k, v in globals().items() if not k.startswith("__")}
        return returning(eval(expression, {"__builtins__": {}}, safe_dict))
    except Exception as e:
        return f"Lỗi: {e}"


# =============================
# Căn bậc n
# =============================
def nth_root(nth: int, number: int):
    getcontext().prec = 8
    result = pow(Decimal(number), (Decimal(1) / Decimal(nth)))
    return int(result) if result == result.to_integral_value() else float(result)


# =============================
# Logarit
# =============================
def log_base(base: float, num: float): return returning(log(num, base))
def ln(num: float): return returning(log(num))


# =============================
# Tổng / Tích liên tục
# =============================
def sigma(first: int, end: int, expression: str, var: str = "i"):
    """Tính tổng ∑"""
    from sympy import symbols, summation, sympify
    i = symbols(var)
    expr = sympify(expression)
    return returning(summation(expr, (i, first, end)))

def continuous_mul(first: int, end: int, expression: str, var: str = "i"):
    """Tính tích ∏"""
    from sympy import symbols, product, sympify
    i = symbols(var)
    expr = sympify(expression)
    return returning(product(expr, (i, first, end)))


# =============================
# Hằng số vật lý
# =============================
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
        "mmHg": 760,
        "inch": 0.0254,
        "lb": 0.45359237,
    }
}

def get_constant(name: str):
    """Tìm giá trị hằng số theo tên (bất kể nhóm)."""
    for group in constants.values():
        if name in group:
            return group[name]
    raise KeyError(f"Hằng số '{name}' không tồn tại.")