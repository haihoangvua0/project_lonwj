""" Backend module for FX-580 simulator (functions collected & refined) """
import math
from decimal import Decimal, getcontext
from polynomial_equations import *
from solving_equations import *

MATH_ERROR = "MATH ERROR"
pi, e = math.pi, math.e

getcontext().prec = 50

# Variable 
variable = [0 for _ in range(10)]
A, B, C, D, E, F, x, y, z, M = variable
names = ["A", "B", "C", "D", "E", "F", "x", "y", "z", "M"]
def stor(**var_input: int):
    global variable, A, B, C, D, E, F, x, y, z, M, names
    # Cập nhật variable theo var_input
    for k, v in var_input.items():
        # Nếu tên biến hợp lệ (A, B, C, D, E, F, x, y, z, M)
        if k in names:
            idx = names.index(k)
            variable[idx] = v
    A, B, C, D, E, F, x, y, z, M = variable
    import os

    # Lấy thư mục chứa file hiện tại
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Nối đường dẫn tuyệt đối tới file muốn mở
    file_path = os.path.join(BASE_DIR, "variable.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        for i in variable:
            f.write(f"{i}\n")
        

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

actual_val_const = {
        "c": 2.99792458e8,
        "g": 9.80665,
        "h": 6.62607015e-34,
        "G": 6.67430e-11,
        "Na": 6.02214076e23,
        "k": 1.380649e-23,
        "R": 8.314462618,
        "eV": 1.602176634e-19,
        "e": 1.602176634e-19,
        "mu_0": 1.25663706212e-6,
        "eps_0": 8.8541878128e-12,
        "KJ": 4.835978484e14,
        "RK": 25812.80745,


        "m_e": 9.1093837015e-31,
        "m_p": 1.67262192369e-27,
        "m_n": 1.67492749804e-27,
        "e_over_me": 1.75882001076e11,
        "u": 1.66053906660e-27,

        "atm": 1.01325e5,
        "Vm": 22.41396954,
        "F": 96485.33212,

        "cal": 4.184,
        "eV": 1.602176634e-19,
        "mmHg": 133.322368,
        "inch": 0.0254,
        "lb": 0.45359237,

        "phi": (1 + 5 ** 0.5) / 2,
        "pi": math.pi,
        "deg_to_rad": math.pi / 180,
        "rad_to_deg": 180 / math.pi,
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
        return abs(float(f) - n) > 1e-50
    except Exception:
        return True

# 5. Unified returning()
def returning(n: int | float | Decimal, choice: str = "S"):
    if isinstance(n, Decimal):
        n = float(n)
    if isinstance(n, int):
        return n
    if math.isnan(n) or math.isinf(n):
        raise ValueError(MATH_ERROR)
    # Xử lí số khoa học =))))
    s = f"{n}"
    if "e" in s:
        s = f"{n:.9e}"
        idx = s.index("e")
        base_ = s[:idx]
        exp_ = s[idx:]
        base_1 = float(base_)
        if abs(base_1 - round(base_1)) < 1e-20:
            base_ = str(int(base_1))
            new_n = float(base_ + exp_)
            return new_n
        else:
            base_ = base_.rstrip("0")
            new_n = float(base_ + exp_)
            return new_n
    if abs(n - round(n)) < 1e-12:
        return int(round(n))
    #temp_ = n / pi
    #if (temp_) == int(temp_) or abs(temp_ - round(temp_)) < 1e-10:
    #    return f"{temp_}pi"
    #del temp_

    if choice.upper() == "S":
        # Chỉ trả về 0 nếu n rất nhỏ (<= 1e-100)
        if abs(n) <= 1e-100:
            return 0
        from fractions import Fraction
        f = Fraction(*n.as_integer_ratio()).limit_denominator()
        if f.denominator == 1:
            return f.numerator
        return f
        # End if choice is 'S'
    # Chỉ trả về 0 nếu n rất nhỏ (<= 1e-100)
    if abs(n) <= 1e-100:
        return 0
    # Nếu là số dạng 1e{a} với -1 <= a < -100, a nguyên, thì trả về số đó luôn
    if n != 0 and isinstance(n, float):
        s = f"{n:.1e}"
        if "e" in s:
            base, exp = s.split("e")
            try:
                exp = int(exp)
                if -100 < exp <= -1 and float(base) == 1.0:
                    return n
            except Exception:
                pass
        del s
    if n > 1e100:
        raise ValueError(MATH_ERROR)
    num = f"{n:.12f}".rstrip("0").rstrip(".")

    actual = float(num)
    if actual == int(actual):
        return int(actual)
    return actual


# 6. Expression engine
def preprocess_expression(expr: str) -> str:
    import re
    expr = re.sub(r'\s+', '', expr)

    # Danh sách hàm multi-char
    funcs = ["sqrt", "sin", "cos", "tan", "asin", "acos", "atan",
             "log", "ln", "exp", "sigma", "cm", "integral", "nth_root"]

    # 1) Thêm * giữa số và hàm:  2sqrt → 2*sqrt
    for f in funcs:
        expr = re.sub(rf'(\d)({f})', rf'\1*\2', expr)

    # 2) Số trước ngoặc
    expr = re.sub(r'(\d)\(', r'\1*(', expr)

    # 3) Ngoặc rồi tới số/biến
    expr = re.sub(r'\)(\d|[A-Za-z])', r')*\1', expr)

    # 4) Số và biến (CHỈ biến 1 ký tự)
    expr = re.sub(r'(\d)([A-Za-z])', r'\1*\2', expr)

    return expr

def evaluate_expression(expr: str, simplify_symbolic=True):
    expr_clean = preprocess_expression(expr)

    from sympy import sympify, radsimp, simplify as sym_simplify
    HAS_SYMPY = True

    if HAS_SYMPY:
        try:
            s = sympify(expr_clean, evaluate=True)

            if simplify_symbolic:
                s = sym_simplify(radsimp(s))

            # Nếu s là số (Integer/Float/Rational) → convert về Python
            if s.is_real:
                # Integer
                if s.is_integer:
                    return int(s)
                # Rational
                if s.is_rational:
                    return float(s)
                # Float
                return float(s)

            # Nếu là biểu thức, trả về chuỗi (hoặc tùy bạn)
            # return str(s)

        except Exception:
            pass

    # Nếu SymPy fail -> eval thủ công
    safe = {
        "sin": sin, "cos": cos, "tan": tan,
        "asin": asin, "acos": acos, "atan": atan,
        "sqrt": sqrt,
        "ln": ln,
        "sigma": sigma,
        "cm": cm,
        "d_dy": d_dy,
        "integral": integral,
        "log": log,
        "nth_root": nth_root,
        "returning": returning,
        "pi": pi,
        "e": e,
    }

    return eval(expr_clean, {"__builtins__": {}}, safe)

def solve_eq(expr: str, var='x'):
    from sympy import sympify, Eq, Symbol, solve
    try:
        expr = expr.replace("^", "**")

        # Nếu không có dấu "=", coi là =0
        if "=" not in expr:
            expr = expr + "=0"

        left, right = expr.split("=")
        left = sympify(left)
        right = sympify(right)
        equation = Eq(left, right)

        symbol = Symbol(var)
        sol = solve(equation, symbol)

        if not sol:
            return MATH_ERROR

        # Chỉ trả nghiệm thực đầu tiên
        for s in sol:
            if s.is_real:
                x = float(s)
                stor(x=x)
                return x

        return MATH_ERROR
    except Exception:
        return MATH_ERROR


# 7. Roots
def exp(n: int | float):
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

def fact(n: int, primes=None):
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

def sqrt(n: int | float):
    if n < 0: return MATH_ERROR
    return (math.sqrt(n))

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
    return (log(math.e, num))

def d_dy(expression: str, var: str = "x"):# val: int = 0):
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
def sigma(first: int, end: int, expression: str, var: str = "x"):
    from sympy import symbols, summation, sympify
    i = symbols(var)
    expr = sympify(expression)
    return returning(summation(expr, (i, first, end)))

def cm(first: int, end: int, expression: str, var: str = "x"):
    from sympy import symbols, product, sympify
    i = symbols(var)
    expr = sympify(expression)
    return returning(product(expr, (i, first, end)))

#calc...
def calc(expr: str, **vars_values):
    from sympy import sympify
    expr = preprocess_expression(expr)
    # Biến đổi ^ thành ** cho hợp cú pháp Python
    expr = expr.replace("^", "**")

    # Tách các biến từ chuỗi
    symbols = list(sympify(expr).free_symbols)
    global actual_val_const
    if not symbols:
        # Biểu thức không có biến
        # Hỗ trợ các hàm toán học và biến đặc biệt như sqrt, sin, cos, pi, e
        safe_dict = {
            "sin": sin,
            "cos": cos,
            "tan": tan,
            "asin": asin,
            "acos": acos,
            "atan": atan,
            "sqrt": sqrt,
            "ln": ln,
            "sigma": sigma,
            "cm": cm,
            "d_dy": d_dy,
            "integral": integral,
            "log": log,
            "nth_root": nth_root,
            "returning": returning,
            "pi": pi,
            "e": e,
        }
        #safe_dict.update(vars_values)
        #safe_dict.update({"pi": math.pi, "e": math.e})

        all_safe = safe_dict | actual_val_const
        val = eval(expr, {"__builtins__": None}, all_safe)
        return val
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
            return MATH_ERROR

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
            "sigma": sigma,
            "cm": cm,
            "d_dy": d_dy,
            "integral": integral,
            "log": log,
            "nth_root": nth_root,
            "returning": returning,
            "pi": pi,
            "e": e,
        }
        avail_var |= vars_values; avail_var |= actual_val_const
        stor(**avail_var)
        local_dict.update(avail_var)
        expr_sp = sympify(expr, locals=local_dict)
        # Nếu expr_sp là số thực (float/int), trả về luôn, nếu không thì evalf
        if isinstance(expr_sp, (int, float)):
            return returning(expr_sp)
        val = expr_sp.evalf(subs=vars_values)
        return float(val)

# Update số khi khởi đầu.
def rcl():
    global variable
    import os

    # Lấy thư mục chứa file hiện tại
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Nối đường dẫn tuyệt đối tới file muốn mở
    file_path = os.path.join(BASE_DIR, "variable.txt")

    with open(file_path, "r", encoding="utf-8") as f:
        variable = list(map(returning, map(evaluate_expression, f.read().splitlines())))
rcl()
# Debug time.
if __name__ == "__main__":
    from sympy import sympify
    print("### Calculator run and test ###")
    print("Choose mode: ")
    while True:
        print("1. Calculate\n2. Complex\n3. Base-N\n4. Matrix\n5. Vector\n6. Statistics\n7. Distribution\n8. Table\n9. Equation(s)\n10. Inequality\n11. Verify\n\"quit\": exit")
        choice = input("Input: ")
        if choice.strip() == "quit":
            print("See ya =))))")
            break
        if choice.strip() == "1":
            print("If you wanna calculate expression with variable\nthen add \"[calc]\" at the end.\n\"mode\" to return.")
            while True:
                expr = input("Input expression: ")
                if expr.strip() == "mode":
                    break
                
                expr = preprocess_expression(expr)
                f_symbol = list(sympify(expr).free_symbols)
                if any((not (i in names)) for i in f_symbol):
                    print(MATH_ERROR); from time import sleep; sleep(2)
                else:
                    if not f_symbol:
                        print("Result:", evaluate_expression(expr))
                    else:
                        if "[calc]" in expr:
                            val_v = {}
                            print("Input value of variable.")
                            for v in f_symbol:
                                v_in = input(f"{v} = ")
                                if v_in.strip() == "":
                                    continue
                                val_v.update({v, returning(v_in)})
                            print("Result:", calc(expression))
        elif choice.strip() == "2":
            print("UPDATING...")
        elif choice.strip() == "3":
            print("UPDATING...")
        elif choice.strip() == "4":
            print("UPDATING...")
        elif choice.strip() == "5":
            print("UPDATING...")
        elif choice.strip() == "6":
            print("UPDATING...")
        elif choice.strip() == "7":
            print("UPDATING...")
        elif choice.strip() == "8":
            print("UPDATING...")
        elif choice.strip() == "9":
            print("UPDATING...")
        elif choice.strip() == "10":
            print("UPDATING...")
        elif choice.strip() == "11":
            print("UPDATING...")