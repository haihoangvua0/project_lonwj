# casio_core.py
# Backend module for FX-580 simulator (functions collected & refined)
import math
from decimal import Decimal, getcontext


MATH_ERROR = "MATH ERROR"
pi, e = math.pi, math.e

getcontext().prec = 12

# Variable 
variable = [0 for _ in range(10)]
A, B, C, D, E, F, x, y, z, M = variable
def stor(**var_input: int):
    global variable, A, B, C, D, E, F, x, y, z, M
    names = ["A", "B", "C", "D", "E", "F", "x", "y", "z", "M"]
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
    file_path = os.path.join(BASE_DIR, "draft.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        for i in variable:
            f.write(f"{i}\n")

def rcl(var: str): pass
    
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
        from sympy import sympify, radsimp, simplify
        HAS_SYMPY = True
    except Exception:
        HAS_SYMPY = False
    if HAS_SYMPY:
        try:
            s = sympify(expr_clean, evaluate=True)
            if simplify_symbolic:
                return simplify(radsimp(s))
            return s
        except Exception:
            pass
    try:
        safe = {
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
        safe.update({"pi": pi, "e": e})
        return eval(expr_clean, {"__builtins__": {}}, safe)
    except Exception:
        return MATH_ERROR

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
                stor(x)
                return x
        
        return MATH_ERROR
    except Exception:
        return MATH_ERROR


# 7. Roots
def exp(n: int | float):
    return math.exp(n)

def fact_(n: int):
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

# Hàm phân tích thừa số nguyên tố cho n rất lớn (n <= 10**10) dùng thuật toán Pollard's Rho
# Miller-Rabin là thuật toán kiểm tra số nguyên tố xác suất (probabilistic), tức là có xác suất nhỏ trả về kết quả sai (số tổng hợp bị nhận nhầm là nguyên tố), nhưng với số lần lặp đủ lớn thì xác suất sai rất nhỏ, gần như không đáng kể với thực tế. Sàng kiểu "chia thử" (trial division) như đoạn code trên là chính xác tuyệt đối, nhưng chậm hơn nhiều cho số lớn.

# Nếu bạn muốn kiểm tra nguyên tố hoặc phân tích thừa số cho n <= 10**10 mà không dùng random, có thể dùng sàng Eratosthenes để tạo bảng các số nguyên tố nhỏ trước (ví dụ tới 10**6), sau đó chia thử với các số nguyên tố này, phần còn lại nếu lớn hơn 1 thì kiểm tra tiếp bằng các thuật toán phân tích thừa số xác định như Fermat, hoặc dùng sàng phân tích thừa số (Sieve Factorization) - nhưng các thuật toán này đều chậm hơn Pollard's Rho với số lớn.

# Để phân tích thừa số n <= 10**10 mà không dùng random, bạn có thể dùng:
# - Sàng Eratosthenes để lấy tất cả prime <= sqrt(n)
# - Chia thử với từng prime đó
# - Nếu còn lại một số lớn hơn 1, kiểm tra nó có phải nguyên tố không (bằng Miller-Rabin deterministic cho n <= 10**16, hoặc AKS cho mọi n nhưng rất chậm)

# Dưới đây là hàm phân tích thừa số không dùng random, chỉ chia thử với prime nhỏ (tối ưu cho n <= 10**10):

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


    # Biến đổi ^ thành ** cho hợp cú pháp Python
    expr = expr.replace("^", "**")

    # Tách các biến từ chuỗi
    symbols = list(sympify(expr).free_symbols)

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
        val = eval(expr, {"__builtins__": None}, safe_dict)
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
        avail_var.update(vars_values)
        stor(**avail_var)
        local_dict.update(avail_var)
        expr_sp = sympify(expr, locals=local_dict)
        # Nếu expr_sp là số thực (float/int), trả về luôn, nếu không thì evalf
        if isinstance(expr_sp, (int, float)):
            return returning(expr_sp)
        val = expr_sp.evalf(subs=vars_values)
        return float(val)

#print(calc("sqrt(x)", x = 9))

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
    for expr in ["x", "x**2"]:
        print(f"sigma(1, 5, '{expr}') = {sigma(1, 5, expr)}")

    print("\n=== Debug: continuous_mul ===")
    for expr in ["x", "x+1"]:
        print(f"cm(1, 4, '{expr}') = {cm(1, 4, expr)}")
set_angle_mode("DEG")

# Mấy hàm cấp cao thì thôi, khỏi nói làm gì, do... nó tốn RAM chạy, mà lỡ đoạn code root này mình áp dụng được lên bo mạch được để tạo ra máy tính mới thì chắc cháy máy. Mình còn đoạn giải phương trình bậc 2, mà bậc 3 thì chưa có. Thêm giúp mình nha.
