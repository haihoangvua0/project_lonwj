#print("RUNNING...")
""" Backend module for FX-580 simulator (functions collected & refined) """
import math
from decimal import Decimal, getcontext
import os
from fractions import Fraction
from decimal import Decimal
import cmath

#from matrix import *
MATH_ERROR = "MATH ERROR"
pi, e = math.pi, math.e

getcontext().prec = 50

app = False
complex_choice = True
def app_open(choice: int = 0):
    global app
    app = (choice == True)
    # Lấy thư mục chứa file hiện tại
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Nối đường dẫn tuyệt đối tới file muốn mở
    file_path = os.path.join(BASE_DIR, "app_choice.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(choice))
app_open(0)
def stor_cmplx(choice: int = 0):
    global complex_choice

    complex_choice = (choice == True)
    # Lấy thư mục chứa file hiện tại
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Nối đường dẫn tuyệt đối tới file muốn mở
    file_path = os.path.join(BASE_DIR, "cmplx_choice.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(choice))
stor_cmplx(0)
# Variable
variable = [0 for _ in range(10)]
A, B, C, D, E, F, x, y, z, M = variable
names = ["A", "B", "C", "D", "E", "F", "x", "y", "z", "M"]
Ans = 0
#PreAns = 0

def stor(**var_input: int):
    global variable, A, B, C, D, E, F, x, y, z, M, names
    # Cập nhật variable theo var_input
    for k, v in var_input.items():
        # Nếu tên biến hợp lệ (A, B, C, D, E, F, x, y, z, M)
        if k in names:
            idx = names.index(k)
            variable[idx] = v
    A, B, C, D, E, F, x, y, z, M = variable

    # Lấy thư mục chứa file hiện tại
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Nối đường dẫn tuyệt đối tới file muốn mở
    file_path = os.path.join(BASE_DIR, "variable.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        for i in variable:
            f.write(f"{i}\n")


# 1. Constants
actual_val_const = {
    # =========================
    # 1. Universal constants
    # =========================
    "h": 6.62607004e-34,          # Planck constant
    "h_": 1.0545718e-34,          # Reduced Planck constant
    "C_0": 299792458,             # Speed of light in vacuum
    "eps_0": 8.854187817e-12,     # Electric permittivity of vacuum
    "mu_0": 1.256637061e-6,       # Magnetic constant
    "Z_0": 376.7303135,           # Vacuum impedance
    "G": 6.67408e-11,             # Newton gravitational constant
    "lp": 1.6162293e-35,          # Planck length
    "tp": 5.39116e-44,            # Planck time

    # =========================
    # 2. Electromagnetic constants
    # =========================
    "muN": 5.050783699e-27,       # Nuclear magneton
    "muB": 9.274009994e-24,       # Bohr magneton
    "e_": 1.602176621e-19,        # Elementary charge
    "phi_0": 2.067833831e-15,     # Magnetic flux quantum
    "G_0": 7.748091731e-5,        # Conductance quantum
    "K_j": 4.835978525e14,        # Josephson constant
    "R_k": 25812.80746,           # von Klitzing constant

    # =========================
    # 3. Atomic & Nuclear physics
    # =========================
    "mp": 1.672621898e-27,        # Proton mass
    "mn": 1.674927471e-27,        # Neutron mass
    "me": 9.10938356e-31,         # Electron mass
    "m_mu": 1.883531594e-28,      # Muon mass
    "m_tau": 3.16747e-27,         # Tau mass
    "a0": 5.291772107e-11,        # Bohr radius
    "alpha": 7.297352566e-3,      # Fine-structure constant
    "re": 2.817940323e-15,        # Classical electron radius
    "lambda_c": 2.426310237e-12,  # Compton wavelength electron
    "gamma_p": 267522190,         # Proton gyromagnetic ratio
    "lambda_cp": 1.321409854e-15, # Proton Compton wavelength
    "lambda_cn": 1.319590905e-15, # Neutron Compton wavelength
    "R_inf": 10973731.57,         # Rydberg constant
    "mu_p": 1.410606787e-26,      # Proton magnetic moment
    "mu_e": -9.28476462e-24,      # Electron magnetic moment
    "mu_n": -9.662365e-27,        # Neutron magnetic moment
    "mu_mu": -4.49044826e-26,     # Muon magnetic moment

    # =========================
    # 4. Physics–Chemistry constants
    # =========================
    "u": 1.66053904e-27,          # Atomic mass unit
    "f": 96485.33289,             # Faraday constant
    "NA": 6.022140857e23,         # Avogadro constant
    "k": 1.38064852e-23,          # Boltzmann constant
    "Vm": 0.022710947,            # Molar gas volume (STP)
    "R": 8.3144598,               # Gas constant
    "C_1": 3.74177179e-16,        # First radiation constant
    "C_2": 0.0143877736,          # Second radiation constant
    "sigma": 5.670367e-8,         # Stefan-Boltzmann constant

    # =========================
    # 5. Adopted values
    # =========================
    "g": 9.80665,                 # Standard gravity
    "atm": 101325,                # Standard atmosphere
    "R_k90": 25812.807,           # Conventional Von Klitzing (1990)
    "K_j90": 4.835979e14,         # Conventional Josephson (1990)

    # =========================
    # 6. Other
    # =========================
    "t": 273.15                  # Celsius -> Kelvin offset
}
# 2. Angle mode (global)
ANGLE_MODE = "DEG"

def set_angle_mode(mode: str):
    global ANGLE_MODE
    mode = mode.strip().upper()
    if mode not in ("DEG", "RAD", "GRA"):
        raise ValueError(MATH_ERROR)
    ANGLE_MODE = mode

    # Lấy thư mục chứa file hiện tại
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Nối đường dẫn tuyệt đối tới file muốn mở
    file_path = os.path.join(BASE_DIR, "mode_angle.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(ANGLE_MODE)
set_angle_mode("DEG")

def _to_radian_if_needed(x: float):
    global ANGLE_MODE
    if ANGLE_MODE == "DEG":
        return math.radians(x)
    if ANGLE_MODE == "GRA":
        return x * math.pi / 200
    return x

# 3. Trig functions (Casio-compatible) + Hypebolic Funcs
def sin(x: float): return math.sin(_to_radian_if_needed(x))
def cos(x: float): return math.cos(_to_radian_if_needed(x))
def tan(x: float):
    a = _to_radian_if_needed(x)
    if math.isclose(math.cos(a), 0, abs_tol=1e-15):
        return float("inf")
    return math.tan(a)

def asin(x: float):
    v = math.asin(x)
    if ANGLE_MODE == "DEG":
        return math.degrees(v)
    if ANGLE_MODE == "GRA":
        return v * 200 / math.pi
    return v   # RAD

def acos(x: float):
    v = math.acos(x)
    if ANGLE_MODE == "DEG":
        return math.degrees(v)
    if ANGLE_MODE == "GRA":
        return v * 200 / math.pi
    return v   # RAD

def atan(x: float):
    v = math.atan(x)
    if ANGLE_MODE == "DEG":
        return math.degrees(v)
    if ANGLE_MODE == "GRA":
        return v * 200 / math.pi
    return v   # RAD

def sinh(x: float):
    return math.sinh(x)

def cosh(x: float):
    return math.cosh(x)

def tanh(x: float):
    return math.tanh(x)

def asinh(x: float):
    v = math.asinh(x)
    # inverse hyperbolic KHÔNG phụ thuộc chế độ DEG/RAD/GRA
    return v

def acosh(x: float):
    v = math.acosh(x)
    return v

def atanh(x: float):
    v = math.atanh(x)
    return v
# 4. Core helpers

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def is_scientific_notation(n: float) -> float:
    """Handle numbers like 1e-7 to avoid float weirdness."""
    s = f"{n}"
    if "e" not in s:
        return n
    s = f"{n:.12e}"
    base, exp = s.split("e")
    base_f = float(base)
    if abs(base_f - round(base_f)) < 1e-15:
        return float(f"{int(round(base_f))}e{exp}")
    else:
        base = base.rstrip("0")
        return float(f"{base}e{exp}")

# ---------------------------------------------------------
# 5. Unified returning()
# ---------------------------------------------------------

def returning(n: int | float | Decimal | complex,
              choice: str = "S",
              /):
              #app: bool = False):
    """
    Trả về số đã rút gọn.
    - choice="S": ưu tiên dạng Fraction.
    """
    global complex_choice
    # ----------------------
    # 0) Decimal -> float
    # ----------------------
    if isinstance(n, Decimal):
        n = float(n)

    # ----------------------
    # 1) NaN / Inf
    # ----------------------
    if isinstance(n, float) and (math.isnan(n) or math.isinf(n)):
        return float("inf")

    elif isinstance(n, (int, float)):
        # ----------------------
        # 3) Số cực nhỏ
        # ----------------------
        if abs(n) < 1e-100:
            return 0
        # ----------------------
        # 2) Scientific
        # ----------------------

        new_n = is_scientific_notation(n)
        if new_n == n:
            n = new_n
        else: return new_n

        # ----------------------
        # 4) Số nguyên
        # ----------------------
        if abs(n - round(n)) < 1e-12:
            return int(round(n))
    elif isinstance(n, complex):
        if complex_choice:
            raise ValueError(MATH_ERROR)
        new_imag = returning(n.imag)
        new_real = returning(n.real)
        return complex(new_real, new_imag)
    # ----------------------
    # 6) Thử phân tích dạng a*sqrt(b)
    # ----------------------
    if check_irrational(n): 
        new_n = f"{n:.12f}".rstrip("0").rstrip(".")            
        actual1 = float(new_n)
        if abs(actual1 - round(actual1)) < 1e-20:
            return int(round(actual1))
        return actual1
    # ----------------------
    # 5) Dạng hữu tỉ nếu choice="S"
    # ----------------------
    if choice.upper() == "S":
        frac = Fraction(*float(n).as_integer_ratio()).limit_denominator()
        if abs(float(frac) - n) < 1e-15:
            # nếu nguyên
            if frac.denominator == 1:
                return frac.numerator
            return frac

    # ----------------------
    # 7) Fallback: trả số float đẹp -> như comp_returning
    # ----------------------
    s = f"{n:.12f}".rstrip("0").rstrip(".")
    actual = float(s)
    if abs(actual - round(actual)) < 1e-12:
        return int(round(actual))

    return actual

def check_irrational(n: float) -> bool:
    try:
        from fractions import Fraction
        f = Fraction(n).limit_denominator()
        return abs(float(f) - n) > 1e-50
    except Exception:
        return True

# 6. Expression engine
def preprocess_expression(expr: str) -> str:
    import re
    expr = expr.replace("^", "**") 
    expr = re.sub(r'\s+', '', expr)

    funcs = ["sqrt", "sin", "cos", "tan", "asin", "acos", "atan",
             "log", "ln", "exp", "sigma_s", "muls", "integral", "nth_root", "pow", "abs"]
    
    const = list(actual_val_const)
    funcs += const
    #funcs += others

    # -------------------------------
    # 1) Protect scientific numbers
    # -------------------------------
    sci_pattern = re.compile(r'\d+(?:\.\d+)?[e][+-]?\d+')
    sci_tokens = []

    expr = sci_pattern.sub(lambda m: f"__SCI{sci_tokens.append(m.group(0)) or len(sci_tokens)-1}__", expr)

    # -------------------------------
    # 2) Insert multipliers
    # -------------------------------

    # number + function
    for f in funcs:
        expr = re.sub(rf'(\d)({f})', r'\1*\2', expr)

    # number + (
    expr = re.sub(r'(\d)\(', r'\1*(', expr)

    # ) then number or letter
    expr = re.sub(r'\)(\d|[A-Za-z])', r')*\1', expr)

    # number + variable (all letters except e, but e still allowed later)
    # Now we WANT e to be multiplied (because scientific notation was protected)
    expr = re.sub(r'(\d)([A-Za-z])', r'\1*\2', expr)
    # variable + pi
    expr = re.sub(r'([A-Za-z])(?=pi)', r'\1*', expr)

    # -------------------------------
    # 3) Restore scientific numbers
    # -------------------------------
    for i, val in enumerate(sci_tokens):
        expr = expr.replace(f"__SCI{i}__", val)
    return expr

def evaluate_expression(expr: str, simplify_symbolic=True, /):
    global variable, A, B, C, D, E, F, x, y, z, M, names, Ans, app
    expr_clean = preprocess_expression(expr)

    safe = {
        "sin": sin, "cos": cos, "tan": tan,
        "asin": asin, "acos": acos, "atan": atan,
        "sqrt": sqrt,
        "ln": ln,
        "sums": sums,
        "muls": muls,
        "d_dx": d_dx,
        "inte": inte,
        "log": log,
        "nth_root": nth_root,
        "pi": pi,
        "e": e,
        "comb": comb,
        "factorial": factorial,
        "perm": perm, 
        "pow": pow,
        "abs": abs,
        "j": 1j
    }

    avail_vars = {k: v for k, v in zip(names, variable)}
    new_ = avail_vars | {"Ans": Ans} | actual_val_const

    from sympy import sympify, radsimp, simplify as sym_simplify
    HAS_SYMPY = True

    if HAS_SYMPY:
        try:
            s = sympify(expr_clean, evaluate=True)

            if simplify_symbolic:
                s = sym_simplify(radsimp(s))

            # Trường hợp trả về NUMBER thực, không ký hiệu
            if s.is_number and not s.free_symbols:
                return returning(float(s))

            # --- SYMBOLIC + app mode ---
            if app:
                s_str = str(s)

                # nếu chứa sqrt và không chứa biến không hợp lệ
                if "sqrt" in s_str:
                    bad = s.free_symbols - set(avail_vars.keys())
                    if not bad:
                        return s_str

            # Còn lại: trả về dạng float
            s = str(s)

        except Exception as es:
            print(es)

    # Nếu SymPy fail -> eval
    safe |= new_
    res = eval(expr_clean, {"__builtins__": {}}, safe)
    res = returning(res)
    Ans = res
    return res

def solve_eq(expr: str, var='x', *, ask: bool = False, **vars_val):
        global A, B, C, D, E, F, x, y, z, M, actual_val_const, Ans
        from sympy import sympify, Eq, Symbol, solve
    #try:
        expr = expr.replace("^", "**")

        # Nếu không có dấu "=", coi là =0
        if "=" not in expr:
            expr = expr + "=0"

        left, right = expr.split("=")
        left = preprocess_expression(left); right = preprocess_expression(right)
        # Lấy các biến trong biểu thức
        #from sympy import sympify
        symbols_left = list(sympify(left).free_symbols)
        symbols_right = list(sympify(right).free_symbols)
        #all_symbols = set(map(str, symbols_left + symbols_right))

        # Lấy giá trị biến đã lưu (A, B, C, ...)
        avail_var = {
            "A": A,
            "B": B,
            "C": C,
            "D": D,
            "E": E,
            "F": F,
            "y": y,
            "z": z,
            "M": M,
            "Ans": Ans
        }

        # Thay thế các biến đã lưu vào biểu thức
        local_dict = avail_var.copy()
        # Thêm các hằng số toán học nếu cần
        local_dict.update(actual_val_const)
        local_dict.update(vars_val)
        stor(**vars_val)
        left = sympify(left, locals=local_dict)
        right = sympify(right, locals=local_dict)
        equation = Eq(left, right)

        symbol = Symbol(var)
        sol = solve(equation, symbol)

        if not sol:
            return []

        # Chỉ trả nghiệm thực đầu tiên
        
        if ask:
            res = []
            for s in sol:
                re, im = s.as_real_imag()
        
                re_f = float(re.evalf())
                im_f = float(im.evalf())
        
                if abs(im_f) < 1e-50:
                    # nghiệm thực
                    res.append(returning(re_f))
                else:
                    # nghiệm phức
                    res.append(complex(re_f, im_f))
            return res    
        for s in sol:
            if s.is_real: 
                    x_val = returning(evaluate_expression(str(s)))
                    stor(x=x_val)
                    return x_val
        return []
    #except Exception:
        #return MATH_ERROR

# 7. Roots
def exp(n: int | float | Decimal | Fraction | complex):
    global complex_choice, ANGLE_MODE
    if isinstance(n, complex):
        if not complex_choice:
            raise ValueError(MATH_ERROR)
        # Detach:
        new_real_pow = math.exp(n.real)
        x_ = n.imag
        new_imag_pow = returning(math.cos(x_)) + returning(math.sin(x_))*1j
        result = new_real_pow + new_imag_pow
        return result
    return math.exp(n)

# Hàm phân tích thừa số nguyên tố cho n lớn (n <= 10**10)
def sieve_primes(limit: int):
    """Trả về list các prime <= limit."""
    sieve = bytearray(b'\x01') * (limit + 1)
    sieve[0:2] = b'\x00\x00'
    for p in range(2, int(math.isqrt(limit)) + 1):
        if sieve[p]:
            step = p
            start = p*p
            sieve[start: limit+1: step] = b'\x00' * ((limit - start)//step + 1)
    return [i for i, isprime in enumerate(sieve) if isprime]

def FACT(n: int, primes=None):
    """
    Phân tích n (n >= 1) thành các thừa số nguyên tố.
    Trả về list các tuple (prime, exponent) theo thứ tự tăng dần prime.
    Dùng tốt cho n <= 1e10 (với primes precomputed tới 1e5).
    """
    # Precompute primes up to 100000 (sufficient for n <= 1e10)
    _PRIMES_UP_TO_1E5 = sieve_primes(100_000)
    if n < 1:
        raise ValueError("n must be >= 1")
    if primes is None:
        primes = _PRIMES_UP_TO_1E5

    factors = []
    remaining = n

    # thử chia các prime từ danh sách
    for p in primes:
        if p * p > remaining:
            break
        if remaining % p == 0:
            exp = 0
            while remaining % p == 0:
                remaining //= p
                exp += 1
            factors.append((p, exp))
        # small early exit
        if remaining == 1:
            break

    # nếu còn phần > 1 thì đó là một prime (hoặc 1)
    if remaining > 1:
        factors.append((remaining, 1))
    return factors

def sqrt(n: int | float | Decimal | Fraction | complex):
    global complex_choice
    if not complex_choice: raise ValueError(MATH_ERROR)
    elif n < 0: 
        real = abs(n)
        real = returning(math.sqrt(real))
        return real*1j
    elif isinstance(n, complex):
        return cmath.sqrt(n)
    return (math.sqrt(n))

def nth_root(base: int | float, ex: int):
    if not isinstance(ex, int) or ex == 0:
        raise ValueError(MATH_ERROR)
    if base < 0:
        if ex % 2 == 0:
            if not complex_choice:
                raise ValueError(MATH_ERROR + ". The number must be over 0")
            base_ = abs(base)
            base_ = nth_root(base_, ex)
            return base_*1j
    elif ex <= 0:
        raise ValueError(MATH_ERROR)
    result = float(pow(base, 1 / ex))
    return returning(result)

# 8. Differentials + log
def log(base: float, num: float | None = None):
    # Trường hợp chỉ truyền 1 tham số -> log(num) = log_base10(num)
    if num is None:
        num = base      # lúc này "base" chính là số cần log
        base = 10       # mặc định logarithm cơ số 10

    # Kiểm tra hợp lệ
    if base <= 0 or base == 1:
        raise ValueError("Base must be over 0 and not equal to 1")
    if num <= 0:
        raise ValueError("Number needs to be over 0")

    # Tính log
    try:
        return returning(math.log(num, base))
    except Exception:
        raise ValueError(MATH_ERROR)

def ln(num: float):
    if num <= 0:
        raise ValueError("The number must be over 0")
    return (log(math.e, num))

def d_dx(expression: str, val: int | None = None):
    from sympy import symbols, diff, sympify

    x = symbols("x")
    expr = sympify(preprocess_expression(expression))

    # Nếu không truyền giá trị -> trả về biểu thức đạo hàm
    derivative = diff(expr, x)

    if val is None:
        return str(derivative)
    else:
        # Trả về giá trị đạo hàm tại x = val
        try:
            res = derivative.subs(x, val)
            if res.is_real:
                return returning(res)
            else: # if isinstance(res, str):
                return evaluate_expression(str(res)) 
        except Exception:
            raise ValueError(MATH_ERROR + ". The expression needs fix...")
def inte(low: float, high: float, expression: str, var: str = "x"):
    from sympy import symbols, integrate, sympify
    x = symbols(var)
    expr = sympify(preprocess_expression(expression))
    res = (integrate(expr, (x, low, high)))
    if res.is_real:
        return returning(res)
    else: # if isinstance(res, str):
        return evaluate_expression(str(res))

# 9. Tổng / Tích liên tục
def sums(first: int, end: int, expression: str, var: str = "x"):
    from sympy import symbols, summation, sympify
    i = symbols(var)
    expr = sympify(preprocess_expression(expression))
    res = (summation(expr, (i, first, end)))
    if res.is_real:
        return returning(res)
    else: # if isinstance(res, str):
        return evaluate_expression(str(res))

def muls(first: int, end: int, expression: str, var: str = "x"):
    from sympy import symbols, product, sympify
    i = symbols(var)
    expr = sympify(preprocess_expression(expression))
    res = (product(expr, (i, first, end)))
    if res.is_real:
        return returning(res)
    else: # if isinstance(res, str):
        return evaluate_expression(str(res))

#calc...
def calc(expr: str, **vars_values):
    from sympy import sympify
    expr = preprocess_expression(expr)
    # Biến đổi ^ thành ** cho hợp cú pháp Python
    expr = expr.replace("^", "**")

    # Tách các biến từ chuỗi
    symbols = list(sympify(expr).free_symbols)
    global actual_val_const, A, B, C, D, E, F, x, y, z, M
    if not symbols:
        # Biểu thức không có biến
        # Hỗ trợ các hàm toán học và biến đặc biệt như sqrt, sin, cos, pi, e
        return evaluate_expression(expr)
    else:
        # Biểu thức có biến -> cần giá trị
        # Loại biến có sẵn.
        avail_var = {
            "A": A,
            "B": B,
            "C": C,
            "D": D,
            "E": E,
            "F": F,
            "x": x,
            "y": y,
            "z": z,
            "M": M,
        }
        missing_vars = [str(v) for v in symbols if ((temp_ := str(v)) not in vars_values) and (temp_ not in avail_var)]
        if missing_vars:
            raise ValueError(MATH_ERROR)

        # Đảm bảo các hàm lượng giác dùng đúng mode
        # Chuyển các hàm sin, cos, tan sang hàm đã xử lý mode
        local_dict = {
            "sin": sin,
            "cos": cos,
            "tan": tan,
            "asin": asin,
            "acos": acos,
            "atan": atan,
            "sqrt": sqrt,
            "ln": ln,
            "sums": sums,
            "muls": muls,
            "d_dx": d_dx,
            "inte": inte,
            "log": log,
            "nth_root": nth_root,
            "returning": returning,
            "pi": pi,
            "e": e,
            "perm": perm,
            "comb": comb,
            "j": 1j,
            "pow": pow,
            "abs": abs
        }
        avail_var |= vars_values
        stor(**avail_var)
        avail_var |= actual_val_const
        local_dict.update(avail_var)
        expr_sp = sympify(expr, locals=local_dict)
        # Nếu expr_sp là số thực (float/int), trả về luôn, nếu không thì evalf
        if isinstance(expr_sp, (int, float)):
            return returning(float(expr_sp))
        val = expr_sp.evalf(subs=vars_values)
        return returning(float(val))

# Tổ hợp, giai thừa, hoán vị (chập)
def comb(k: int | float, n: int | float):
    try:
        return math.comb(n, k)
    except:
        raise ValueError(MATH_ERROR)

def perm(k: int | float, n: int | float | None = None):
    try:
        return math.perm(n, k)
    except:
        raise ValueError(MATH_ERROR)

def factorial(n: int | float):
    try:
        return math.factorial(n)
    except:
        raise ValueError(MATH_ERROR)

# Update số khi khởi đầu.
def rcl():
    global variable

    # Lấy thư mục chứa file hiện tại
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Nối đường dẫn tuyệt đối tới file muốn mở
    file_path = os.path.join(BASE_DIR, "variable.txt")

    with open(file_path, "r", encoding="utf-8") as f:
        variable = list(map(returning, map(evaluate_expression, f.read().splitlines())))
rcl()
# lst_of_cmd = ["[solve]", '[calc]', "[settings]"]
dict_of_setting = {
    "Angle unit": ANGLE_MODE,
    "Statistics": 0, # Freq on or of
    "Equation/ Function": 0, # Mở kết quả số phức
    "Table": 1 # f(x) / f(x), g(x)
    #"Language" # 1. English/ 2. Tiếng Việt
}
# lst_of_stop = ["stop", "off", "exit", "quit"]
def stat_setting(choice: int = dict_of_setting["Statistics"]):
    global dict_of_setting
    dict_of_setting["Statistics"] = choice

    # Lấy thư mục chứa file hiện tại
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Nối đường dẫn tuyệt đối tới file muốn mở
    file_path = os.path.join(BASE_DIR, "statistics.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"{choice}")
stat_setting(0)

def eq_fu_settings(choice: int = dict_of_setting["Equation/ Function"]):
    global dict_of_setting

    choice = dict_of_setting["Equation/ Function"]
    # Lấy thư mục chứa file hiện tại
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Nối đường dẫn tuyệt đối tới file muốn mở
    file_path = os.path.join(BASE_DIR, "equation_funcs.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"{choice}")
eq_fu_settings(0)

def table_settings(choice: int = dict_of_setting["Table"]):

    # Lấy thư mục chứa file hiện tại
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Nối đường dẫn tuyệt đối tới file muốn mở
    file_path = os.path.join(BASE_DIR, "table.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"{choice}")
table_settings(1)
def stor_settings():
    global ANGLE_MODE, dict_of_setting

    # Lấy thư mục chứa file hiện tại
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Nối đường dẫn tuyệt đối tới file muốn mở
    file_path = os.path.join(BASE_DIR, "mode_angle.txt")

    with open(file_path, "r", encoding="utf-8") as f:
        ANGLE_MODE = f.readline()
        dict_of_setting["Angle unit"] = ANGLE_MODE

    file_path = os.path.join(BASE_DIR, "statistics.txt")

    with open(file_path, "r", encoding="utf-8") as f:
        dict_of_setting["Statistics"] = int(f.readline())

    file_path = os.path.join(BASE_DIR, "equation_funcs.txt")

    with open(file_path, "r", encoding="utf-8") as f:
        dict_of_setting["Equation/ Function"] = int(f.readline())

    file_path = os.path.join(BASE_DIR, "table.txt")

    with open(file_path, "r", encoding="utf-8") as f:
        dict_of_setting["Table"] = int(f.readline())
stor_settings()
# debug line
#from time import sleep
print("Set data")
#sleep(1.5)
print("Debugging...")
res_ = []
res_.append(str(solve_eq("x**2+B", ask=True, B=1))+"\n")
stor(x=sqrt(2)); 
res_.append(str(evaluate_expression("2x+1-3"))+"\n")
res_.append(str(calc("2A - 3", A=6))+"\n")
res_.append(str(returning(sqrt(2)))+"\n")
res_.append(str(d_dx("x^2 + 2x + 1", 9)) + "\n")
res_.append(str(inte(0, 4, "x^2 + 4")) + "\n")
res_.append(str(sums(0, 10, "x**2")) + "\n")
res_.append(str(muls(1, 10, "x")) + "\n")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "run.txt")
with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(res_)
print("Done")
#sleep(1.5)
os.system('cls' if os.name == 'nt' else 'clear')
