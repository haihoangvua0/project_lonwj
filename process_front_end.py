""" Backend module for FX-580 simulator (functions collected & refined) """

# Module needed for all
from functools import cache
import math
from decimal import Decimal, getcontext
import os
from fractions import Fraction
from decimal import Decimal
import cmath
import random

# Symbol
theta_symbol = "\u03B8"     
pi_symbol = "\u03C0"        
degree = "\u00B0"    
angle = "\u2220"     
sqrt_symbol = "\u221A"      

# Default vars needed
Randint = random.randint
Ran_ = random.random()
Rnd = round

MATH_ERROR = "MATH ERROR"
pi = math.pi
gcd = math.gcd
lcm = math.lcm

# Hardware object class
class euler_num:
    def __init__(self):
        self.value = math.e
    def __add__(self, other):
        if isinstance(other, euler_num):
            return self.value + other.value
        return self.value + other
    def __sub__(self, other):
        if isinstance(other, euler_num):
            return self.value - other.value
        return self.value - other
    def __mul__(self, other):
        if isinstance(other, euler_num):
            return self.value * other.value
        return self.value * other
    def __truediv__(self, other):
        if isinstance(other, euler_num):
            return self.value / other.value
        return self.value / other
    def __pow__(self, other):
        if isinstance(other, euler_num):
            return exp(other.value)
        return exp(other)
    def __radd__(self, other):
        if isinstance(other, euler_num):
            return other.value + self.value
        return other + self.value
    def __rsub__(self, other):
        if isinstance(other, euler_num):
            return other.value - self.value
        return other - self.value
    def __rmul__(self, other):
        if isinstance(other, euler_num):
            return other.value * self.value
        return other - self.value
    def __rtruediv__(self, other):
        if isinstance(other, euler_num):
            return other.value / self.value
        return other + self.value
    def __rpow__(self, other):
        if isinstance(other, euler_num):
            return Pow(other.value, self.value)
        return Pow(other, self.value)
    def __repr__(self):
        return f"{self.value}"

    def __float__(self):
        return self.value

    def __int__(self):
        return int(self.value)

    def __str__(self):
        return f"{self.value}"

    def __format__(self, format_spec):
        return format(self.value, format_spec)

    def __eq__(self, other):
        return self.value == other
    
    def __ne__(self, other):
        return not self == other
    
    def __lt__(self, other):
        return self.value < other
    
    def __le__(self, other):
        return self < other or self == other
    
    def __gt__(self, other):
        return not self <= other
    
    def __ge__(self, other):
        return not self < other
complex_choice = False
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

@cache
def split_in_out(n: int):
    out = 1
    ins = 1

    temp_facts = FACT(n)
    for k, v in temp_facts:
        if v % 2 == 0:
            out *= Pow(k, v // 2)
        else:
            out *= Pow(k, (v - 1) // 2)
            ins *= k
    return out, ins
class sqrt:
    def __init__(self, n: int | float | list | Fraction | Decimal | complex):
        #self.original = n
        self.val = None

        # mặc định
        self.coef = None
        self.radicand = None
        self.sums_terms = None
        # ===== REAL =====
        if isinstance(n, (int, float, Fraction, Decimal)):
            self.val = customised_sqrt(n)
            if n >= 0:
                if isinstance(n, int): 
                    out, ins = split_in_out(n)
                    self.coef = out
                    self.radicand = ins
                elif isinstance(n, (float, Decimal)):
                    n = float(n)
                    if check_irrational(n):
                        self.coef = self.val
                        self.radicand = 1
                    else:
                        n = Fraction(*n.as_integer_ratio()).limit_denominator()
                        out_de, ins_de = split_in_out(n.denominator)
                        numerator = n.numerator * ins_de
                        out_nu, ins_nu = split_in_out(numerator)
                        new_frac = Fraction(out_nu, out_de*ins_de).limit_denominator()
                        if new_frac.denominator == 1:
                            self.coef = new_frac.numerator
                            self.radicand = ins_nu
                        else:
                            self.coef = new_frac
                            self.radicand = ins_nu
                elif isinstance(n, Fraction):
                        temp_facts_denominator = FACT(n.denominator)
                        ins_de = []
                        ins_de_int = 1
                        out_de = 1
                        for k, v in temp_facts_denominator:
                            if v % 2 == 0:
                                out_de *= Pow(k, v // 2)
                            else:
                                out_de *= Pow(k, (v - 1) // 2)
                                ins_de.append((k, 1))
                                ins_de_int *= k
                        #self.radicand
                        temp_facts_numerator = FACT(n.numerator) + ins_de
                        ins_nu = 1
                        out_nu = 1
                        for k, v in temp_facts_numerator:
                            if v % 2 == 0:
                                out_nu *= Pow(k, v // 2)
                            else:
                                out_nu *= Pow(k, (v - 1) // 2)
                                ins_nu *= k
                        new_frac = Fraction(out_nu, out_de*ins_de_int).limit_denominator()
                        if new_frac.denominator == 1:
                            self.coef = new_frac.numerator
                            self.radicand = ins_nu
                        else:
                            self.coef = new_frac
                            self.radicand = ins_nu
            else:
                if not complex_choice:
                    raise ValueError(MATH_ERROR)
                out = 1
                ins = 1
                temp_facts = FACT(-n)
                for k, v in temp_facts:
                    if v % 2 == 0:
                        out *= Pow(k, v // 2)
                    else:
                        out *= Pow(k, (v - 1) // 2)
                        ins *= k
                self.coef = out * 1j
                self.radicand = ins
        elif isinstance(n, complex):
            if not complex_choice: raise ValueError(MATH_ERROR)
            self.val = customised_sqrt(n)
            self.coef = self.val
            self.radicand = 1
        elif isinstance(n, list):
            res = 0
            for i in range(len(n)):
                if isinstance(n[i][0], (float, Decimal)):
                        if check_irrational(n[i][0]):
                                pass
                        else:
                                n[i] = (Fraction(*float(n[i][0]).as_integer_ratio()).limit_denominator(), n[i][1])
                res += (n[i][0]*customised_sqrt(n[i][1]))
            self.val = res
            self.sums_terms = n
    @property
    def items(self):
        if self.sums_terms is None \
           and self.coef is not None \
           and self.radicand is not None:
            return [(self.coef, self.radicand)]
        elif self.sums_terms is not None \
           and (self.coef is None \
           or self.radicand is None):
            return self.sums_terms
        else:
            raise ValueError(MATH_ERROR)
    @property
    def value(self): return self.val

    # Printing and formating...
    def __repr__(self):
        return str(self)

    def __str__(self):
        terms = []

        for coef, rad in self.items:
            if isinstance(coef, complex):
                if rad == 1: 
                    c_term = f"{coef}".replace('j','i')
                else:
                    if coef.real == 0 and not coef.imag == 0:
                        c_term = f"({coef.imag}i)*sqrt({rad})"
                    elif coef.real != 0 and coef.imag == 0:
                        c_term = f"{returning(coef.real)}*sqrt({rad})"
                    elif coef.real != 0 and coef.imag != 0:
                        c_term = f"{coef}*sqrt({rad})".replace('j', 'i')
                    else: c_term = ""
                terms.append(c_term)
                continue
            if coef == 0:
                continue

            # ===== RADICAND == 1 -> số thường =====
            if rad == 1:
                term = f"{coef}"
            else:
                # ===== COEF =====
                if coef == 1:
                    term = f"sqrt({rad})"
                elif coef == -1:
                    term = f"-sqrt({rad})"
                else:
                    if isinstance(coef, Fraction): 
                        if coef.denominator != 1:
                            if coef > 0:
                                term = f"({coef})*sqrt({rad})"
                            else: 
                                term = f"-({-coef})*sqrt({rad})"
                        else: term = f"{coef.numerator}*sqrt({rad})"
                    else: term = f"{coef}*sqrt({rad})"

            terms.append(term)

        if not terms:
            return "0"

        # ===== JOIN + FIX DẤU =====
        display = terms[0]
        for t in terms[1:]:
            if t.startswith("-"):
                display += t
            else:
                display += "+" + t

        return display
    
    def __float__(self):
        v = self.value
        if isinstance(v, complex):
            raise ValueError("Cannot convert complex to float")
        return float(v)

    def __int__(self):
        v = self.value
        if isinstance(v, complex):
            raise ValueError("Cannot convert complex to int")
        return int(v)

    def __format__(self, format_spec):
        return format(str(self), format_spec)
    
    # Math doing
    def __add__(self, other):
        if isinstance(other, sqrt):
            items = sorted(self.items + other.items, key=lambda x: x[1])
            now = items[0][1]
            total = 0
            new_terms = []
            for i in range(len(items)):
                if items[i][1] != now:
                    new_terms.append((total, now))
                    now = items[i][1]
                    total = items[i][0]
                else:
                    total += items[i][0]
            new_terms.append((total, now))
            return sqrt(new_terms)
        elif isinstance(other, (int, float, Fraction, Decimal)):
            if other == 0: return self
            if not any(i[1] == 1 for i in self.items):
                new_terms = [(returning(other), 1)] + self.items
                return sqrt(new_terms)
            else:
                items = list(filter(lambda x: x[1] == 1, self.items))
                remain = list(filter(lambda x: not x[1] in [0, 1] and not x[0] == 0, self.items))
                total = sum(x[0] for x in items)
                total += other
                new_terms = [(total, 1)] + remain
                return sqrt(new_terms)
    def __radd__(self, other):
        return self + other
    def __sub__(self, other):
        # a - b -> a + (-b)
        return self + ((-1)*other)
    def __rsub__(self, other):
        return (-1)*self + other
    def __mul__(self, other):
        if isinstance(other, sqrt):
            items_other = other.items
            items_self = self.items
            terms = []
            for i in items_self:
                for j in items_other:
                    out = i[0] * j[0]
                    ins = i[1] * j[1]
                    outside, inside = split_in_out(ins)
                    terms.append((out*outside, inside))
            return sqrt(terms)
        elif isinstance(other, (int, float, Fraction, Decimal, complex)):
            if isinstance(other, (int, float, Fraction, Decimal)):
                if other == 1: return self
                if check_irrational(other): pass
                else: other = Fraction(*float(other).as_integer_ratio()).limit_denominator()
            items = self.items
            new_terms = []
            for i in items:
                outs = other * i[0]
                new_terms.append((outs, i[1]))
            return sqrt(new_terms)
        else: raise ValueError(MATH_ERROR)
    def __rmul__(self, other):
        return self * other
    def __pow__(self, other):
        if isinstance(other, int):
            if 0 <= (other) <= 5:
                res = 1
                for _ in range(other):
                    res *= self
                return res
            else: return Pow(self.value, other)
        elif isinstance(other, (float, Decimal, Fraction)):
            n = float(other)
            return Pow(self.value, n)
        elif isinstance(other, sqrt):
            return Pow(self.value, other.value)
        raise ValueError(MATH_ERROR)
    def __rpow__(self, other):
        return Pow(other, self.value)
    def __truediv__(self, other):
        if isinstance(other, sqrt):
            if len(other.items) == 1:
                items_o = other.items[0]
                items_s = self.items
                res = 0
                for outs, ins in items_s:
                    new_sqrt = sqrt(Fraction(ins, items_o[1]))
                    res += (Fraction(outs, items_o[0])*new_sqrt)
                return res
            if len(other.items) == 2:
                items_o = other.items
                items_s = self.items
                sqrt_needed = sqrt([items_o[0]]) - sqrt([items_o[1]])
                # Tử số
                numerator = self * sqrt_needed
                # Mẫu số
                denominator = other * sqrt_needed
                # Do mẫu đã nhân liên hợp, lúc này chỉ cần chia tử sqrt với number thôi
                value_denominator = denominator.value
                return numerator / value_denominator
            else: return returning(self.value / other.value)
        if isinstance(other, (int, float, Fraction, Decimal)):
            items = self.items
            new_terms = []
            for k, v in items:
                new_terms.append((k/other, v))
            return sqrt(new_terms)
        raise ValueError(MATH_ERROR)
    def __rtruediv__(self, other):
        if len(self.items) == 1:
            ins = self.items[0][1]
            outs = self.items[0][0]
            # Mẫu số
            denominator = outs * ins
            # Tử số
            if isinstance(other, (int, float, Fraction, Decimal)):
                return Fraction(other, denominator).limit_denominator() * sqrt(ins)
            if isinstance(other, sqrt):
                return Fraction(1, denominator) * other * sqrt(ins)
        if len(self.items) == 2:
            sqrt_needed = sqrt([self.items[0]]) - sqrt([self.items[1]])
            # Mẫu số:
            denominator = (self * sqrt_needed)
            val_denominator = denominator.value
            # Tử số:
            numerator = other * sqrt_needed
            return numerator / val_denominator
        else:
            return other / self.value
    def __eq__(self, other):
        if isinstance(other, sqrt):
            return self.value == other.value
        return self.value == other
    
    def __ne__(self, other):
        return not self == other
    
    def __lt__(self, other):
        return self.value < other
    
    def __le__(self, other):
        return self < other or self == other
    
    def __gt__(self, other):
        return not self <= other
    
    def __ge__(self, other):
        return not self < other

# put value.
e = euler_num()
getcontext().prec = 50

app = False
def app_open(choice: int = 0):
    global app
    app = (choice == True)
    # Lấy thư mục chứa file hiện tại
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Nối đường dẫn tuyệt đối tới file muốn mở
    file_path = os.path.join(BASE_DIR, "app_choice.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(choice))
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

def stor_ans():
    stor_ = Ans
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Nối đường dẫn tuyệt đối tới file muốn mở
    file_path = os.path.join(BASE_DIR, "ans.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(stor_))
stor_ans()

def open_ans():
    global Ans
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Nối đường dẫn tuyệt đối tới file muốn mở
    file_path = os.path.join(BASE_DIR, "ans.txt")

    with open(file_path, "r", encoding="utf-8") as f:
        Ans = f.readlines()[-1]
        Ans = evaluate_expression(Ans)


a = {
    "x": 0
}
stor(**a)
del a

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

def convert_deg(x: int | float | Fraction | Decimal):
    if ANGLE_MODE == "DEG":
        return returning(math.degrees(x))
    if ANGLE_MODE == "GRA":
        return returning(x * 200 / pi)
    return returning(x)   # RAD
# 3. Trig functions (Casio-compatible) + Hypebolic Funcs
def sin(x: float):
    a = _to_radian_if_needed(x)

    k = round(a / pi)
    if abs(a - k * pi) <= 1e-12:
        return 0

    return returning(math.sin(a))
def cos(x: float):
    a = _to_radian_if_needed(x)

    k = round((a - pi/2) / pi)
    if abs(a - (pi/2 + k * pi)) <= 1e-12:
        return 0

    return returning(math.cos(a))
def tan(x: float):
    a = _to_radian_if_needed(x)
    if math.isclose(math.cos(a), 0, abs_tol=1e-15):
        return float("inf")
    return returning(math.tan(a))

def asin(x: float):
    v = math.asin(x)
    return convert_deg(v)   # RAD

def acos(x: float):
    v = math.acos(x)
    return convert_deg(v)

def atan(x: float):
    v = math.atan(x)
    return convert_deg(v)

def sinh(x: float):
    return returning(math.sinh(x))

def cosh(x: float):
    return returning(math.cosh(x))

def tanh(x: float):
    return returning(math.tanh(x))

def asinh(x: float):
    v = math.asinh(x)
    # inverse hyperbolic KHÔNG phụ thuộc chế độ DEG/RAD/GRA
    return returning(v)

def acosh(x: float):
    v = math.acosh(x)
    return returning(v)

def atanh(x: float):
    v = math.atanh(x)
    return returning(v)
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

def returning(n: int | float | Decimal | sqrt | complex,
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
        n = float(n)
        if n >= 1e100: return float("inf")
        elif n <= -1e100: return float("-inf")
        elif "e" in str(n):
            new_n = is_scientific_notation(n)
            return new_n

        # ----------------------
        # 4) Số nguyên
        # ----------------------
        if abs(n - round(n)) < 1e-12:
            return int(round(n))
    elif isinstance(n, complex):
        if not complex_choice:
            raise ValueError(MATH_ERROR)
        return n
    elif isinstance(n, sqrt):
        if choice == "D":
            return n.value
        elif choice == "S":
            return n
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

# =========================
# Chia lấy dư và hệ toạ độ Đề-các
def Pol(x: int | float | Fraction | Decimal, y: int | Fraction | float | Decimal, ask: bool = False):
    import math
    r = returning(math.hypot(x, y))
    theta = returning(convert_deg(math.atan2(y, x)))
    if ask:
        return r, theta, "pol"
    elif complex_choice:
        return r, theta
    return r

def Rec(r: int | float | Fraction | Decimal, theta: int | float | Fraction | Decimal, ask: bool = False):
    import math
    theta = _to_radian_if_needed(theta)
    x = returning(r * math.cos(theta))
    y = returning(r * math.sin(theta))
    if ask:
        return x, y, "rec"
    elif complex_choice:
        return x, y
    return returning(x)

# =========================
# Complex process
# =========================

# Real part:
def ReP(z: int | float | Fraction | complex | str):
    if complex_choice:
        if isinstance(z, complex):
            return returning(z.real)
        elif isinstance(z, str):
            if angle in z:
                r, t = map(returning, z.split(angle))
                re, _ = Rec(r, t)
                return returning(re)
            else: raise ValueError(MATH_ERROR)
        else:
            return returning(z)
    else: raise ValueError(MATH_ERROR)
def ImP(z: int | float | Fraction | complex | str):
    if complex_choice:
        if isinstance(z, complex):
            return returning(z.imag)
        elif isinstance(z, str):
            if angle in z:
                r, t = map(returning, z.split(angle))
                _, im = Rec(r, t)
                return returning(im)
            else:
                return evaluate_expression(z)
        else:
            return returning(z)
    else: raise ValueError(MATH_ERROR)

def Arg(z: complex | int | float | Fraction | str):
    if complex_choice:
        if isinstance(z, complex):
            _, theta = Pol(z.real, z.imag)
            return theta
        elif isinstance(z, str):
            if angle in z:
                _, t = map(returning, z.split(angle))
                return returning(t)
            else:
                return evaluate_expression(z)
        else:
            return 0
    else: return 0

def Conjg(z: int | float | Fraction | complex | str):
    if complex_choice:
        if isinstance(z, complex):
            return z.conjugate()
        elif isinstance(z, str):
            if angle in z:
                r, t = map(returning, z.split(angle))
                re, im = Rec(r, t)
                new_cmplx = complex(re, im)
                return new_cmplx.conjugate()
            else: return evaluate_expression(z)
        else: return returning(z)
    else:
        raise ValueError(MATH_ERROR)

def modulo(a: int, b: int, /, ask: bool = False):
    if complex_choice and not not b != 0:
        raise ValueError(MATH_ERROR)
    res = a // b
    if a < 0 or b < 0:
        return returning(res)
    remain = a - res * b
    if ask:
        return res, remain, "mod"
    return res

# 6. Expression engine
def preprocess_expression(expr: str) -> str: 
    global names 
    import re  

    #expr = expr.replace("^", "**")  
    expr = re.sub(r'\s+', '', expr) 
    expr = expr.replace("×", "*") 
    # -------------------------------  
    # protect expression argument in inte()  
    # inte(a,b,expr)  -> inte(a,b,"expr")  
    # -------------------------------  
    def repl_inte(m):  
        low, high, expr = m.groups()  
        return f'inte({low},{high},"{expr}")'  

    expr = re.sub(  
        r'inte\(\s*([^,]+)\s*,\s*([^,]+)\s*,\s*(.+)\s*\)$',  
        repl_inte,  
        expr  
    )  
    def repl_sigma(m):  
        low, high, expr = m.groups()  
        return f'sums({low},{high},"{expr}")'  

    expr = re.sub(  
        r'sums\(\s*([^,]+)\s*,\s*([^,]+)\s*,\s*(.+)\s*\)$',  
        repl_sigma,  
        expr  
    )  
    def repl_muls(m):  
        low, high, expr = m.groups()  
        return f'muls({low},{high},"{expr}")'  

    expr = re.sub(  
        r'muls\(\s*([^,]+)\s*,\s*([^,]+)\s*,\s*(.+)\s*\)$',  
        repl_muls,  
        expr  
    )   
    def repl_diff(m):  
        expr, val = m.groups()  
        return f'd_dx("{expr}", {val})'  

    expr = re.sub(  
        r'd_dx\(\s*(.+?)\s*,\s*([^)]+)\s*\)',  
        repl_diff,  
        expr  
    )  

    pattern = re.compile(r'\|([^|]+)\|')  

    while pattern.search(expr):  
        expr = pattern.sub(r'abs(\1)', expr)  
    # -------------------------------  
    # factorial (Casio-style)  
    # -------------------------------  
    while '!' in expr:  
        expr = re.sub(  
            r'(\([^()]+\)|[A-Za-z0-9_.]+)!',  
            r'factorial(\1)',  
            expr  
        )  
    # (biểu thức)%  ->  (biểu thức)/100  
    while "%" in expr:  
        expr = re.sub(  
            r'(\([^()]+\)|[A-Za-z0-9_.]+)%',  
            r'(\1)/100',  
            expr  
        )  
    # Chia lấy dư và lấy nguyên ([mod])  
    # PURE mod: chỉ có a[mod]b  
    pure_mod = re.fullmatch(  
        r'(\([^|]+\)|[A-Za-z0-9_.]+)\[mod\](\([^|]+\)|[A-Za-z0-9_.]+)',  
        expr  
    )  
    if pure_mod:  
        a, b = pure_mod.groups()  
        return f"modulo({a},{b},ask=True)"  

    mod_pattern = re.compile(r'(\([^|]+\)|[A-Za-z0-9_.]+)\[mod\](\([^|]+\)|[A-Za-z0-9_.]+)')  
    # mod trong biểu thức  
    while mod_pattern.search(expr):  
        expr = mod_pattern.sub(  
            r'modulo(\1,\2)',  
            expr  
        )  

    # x2 độ gian nan với Pol và Rec  
    pure_pol = re.fullmatch(  
        r'Pol\(([^()]+),([^()]+)\)',  
        expr  
    )  
    if pure_pol:  
        a, b = pure_pol.groups()  
        return f"Pol({a},{b},True)"  

    pure_rec = re.fullmatch(  
        r'Rec\(([^()]+),([^()]+)\)',  
        expr  
    )  
    if pure_rec:  
        a, b = pure_rec.groups()  
        return f"Rec({a},{b},True)"  
    # -------------------------------  
    # nCr / nPr  
    # -------------------------------  
    expr = re.sub(  
        r'(\([^()]+\)|[A-Za-z0-9_.]+)_C_(\([^()]+\)|[A-Za-z0-9_.]+)',  
        r'comb(\1,\2)',  
        expr  
    )  
    expr = re.sub(  
        r'(\([^()]+\)|[A-Za-z0-9_.]+)_P_(\([^()]+\)|[A-Za-z0-9_.]+)',  
        r'perm(\1,\2)',  
        expr  
    )  

    # -------------------------------  
    # power **  
    # -------------------------------  
    func_calls = []  
    def protect_func(m):  
        func_calls.append(m.group(0))  
        return f"__FUNC{len(func_calls)-1}__"  

    expr = re.sub(  
        r'[A-Za-z_]+\([^()]*\)',  
        protect_func,  
        expr  
    )  
    def find_matching_paren(s: str, open_idx: int) -> int:
        depth = 1
        i = open_idx + 1
        while i < len(s):
            if s[i] == '(':
                depth += 1
            elif s[i] == ')':
                depth -= 1
                if depth == 0:
                    return i
            i += 1
        raise ValueError("Unmatched parenthesis in power")

    def find_base_start(s: str, caret_idx: int) -> int:
        """
        caret_idx trỏ vào '^'
        tìm base ngay trước nó
        """
        i = caret_idx - 1

        # case 1: base là ngoặc đóng (...)
        if i >= 0 and s[i] == ')':
            depth = 1
            i -= 1
            while i >= 0:
                if s[i] == ')':
                    depth += 1
                elif s[i] == '(':
                    depth -= 1
                    if depth == 0:
                        return i
                i -= 1
            raise ValueError("Unmatched parenthesis in base")

        # case 2: base là symbol / number
        while i >= 0 and (s[i].isalnum() or s[i] in '._'):
            i -= 1
        return i + 1

    def parse_power(expr: str) -> str:
        while '^(' in expr:
            idx = expr.rfind('^(')   # PHẢI NHẤT -> right associative

            base_start = find_base_start(expr, idx)
            base = expr[base_start:idx]

            open_paren = idx + 1  # trỏ vào '('
            close_paren = find_matching_paren(expr, open_paren)

            exponent = expr[open_paren + 1:close_paren]

            replacement = f'(Pow({base},{exponent}))'

            expr = (
                expr[:base_start]
                + replacement
                + expr[close_paren + 1:]
            )

        return expr
    # Do scientific num is protected -> ...
    expr = parse_power(expr)
    for i, f in enumerate(func_calls):  
        expr = expr.replace(f"__FUNC{i}__", f)  
    # -------------------------------  
    # protect scientific notation  
    # -------------------------------  
    sci_pattern = re.compile(r'\d+(?:\.\d+)?e[+-]?\d+')  
    sci_tokens = []  
    expr = sci_pattern.sub(  
        lambda m: f"__SCI{sci_tokens.append(m.group(0)) or len(sci_tokens)-1}__",  
        expr  
    )  

    funcs = [  
        "sqrt", "sin", "cos", "tan", "asin", "acos", "atan",  
        "log", "ln", "exp", "sums", "muls", "integral",  
        "nth_rt", "pow", "Pow", "abs", "factorial", "gcd", "lcm",  
        "modulo"  
    ] + list(actual_val_const)  

    for f in sorted(funcs, key=len, reverse=True):  
        expr = re.sub(rf'(\d)({f})', r'\1*\2', expr) 
    # -------------------------------  
    # implicit multiplication  
    # -------------------------------   
    expr = re.sub(r'(\d)\(', r'\1*(', expr)  
    expr = re.sub(r'\)(\d|[A-Za-z])', r')*\1', expr)  
    expr = re.sub(r'(\d)([A-Za-z])', r'\1*\2', expr)  
    #expr = re.sub(r'([A-Za-z])(?=pi)', r'\1*', expr)  
    new = names + ["pi", "e", "Ans"]
    for i in sorted(new, key=len, reverse=True):
        if re.compile(r"({i})([A-Za-z])"): continue
        expr = re.sub(rf"([A-Za-z0-9_.])({i})", r"\1*\2", expr)
    # -------------------------------  
    # restore scientific notation  
    # -------------------------------  
    for i, val in enumerate(sci_tokens):  
        expr = expr.replace(f"__SCI{i}__", val)  

    return expr

def evaluate_expression(expr: str,
                        *,
                        simplify_symbolic=True):
    global variable, A, B, C, D, E, F, x, y, z, M, names, Ans, app
    expr_clean = preprocess_expression(expr)
    safe = {
        "sin": sin, "cos": cos, "tan": tan,
        "asin": asin, "acos": acos, "atan": atan,
        "ln": ln,
        "sums": sums,
        "muls": muls,
        "d_dx": d_dx,
        "inte": inte,
        "log": log,
        "comb": comb,
        "factorial": factorial,
        "perm": perm, 
        "pow": Pow,
        "Pow": Pow,
        "abs": abs,
        #"frac": Fraction,
        "nth_rt": nth_root,
        "gcd": gcd,
        "lcm": lcm,
        "RandInt": Randint,
        "Int": int,
        "Rnd": Rnd,
        "Rec": Rec,
        "Pol": Pol,
        "modulo": modulo,
        "sqrt": sqrt,
        "exp": exp
    }
    if complex_choice:
        safe.pop("Rec")
        safe.pop("Pol")
        safe.update({
            "ImP": ImP,
            "ReP": ReP,
            "Arg": Arg,
            "Conjg": Conjg
        })
    new_ = {"Ans": Ans} | actual_val_const
    safe.update({
        "pi": pi,
        "e": e,
        "Ran#": Ran_
    } | ({
        "i": 1j
    } if complex_choice else {}))
    # Nếu SymPy fail -> eval
    avail_vars = {k: v for k, v in zip(names, variable)}
    new_ |= avail_vars
    safe |= new_
    res = eval(expr_clean, {"__builtins__": {}}, safe)
    if isinstance(res, (tuple, list, dict, str, set, range)): return res
    res = returning(res)
    Ans = res
    return res

def solve_eq(expr: str, var='x', *, ask: bool = False, **vars_val):
    global A, B, C, D, E, F, x, y, z, M, actual_val_const, Ans
    from sympy import sympify, Eq, Symbol, solve
    #try:
    #expr = expr.replace("^", "**")

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
    }
    FUNC_MAP = {
        "sin": sin, "cos": cos, "tan": tan,
        "asin": asin, "acos": acos, "atan": atan,
        "ln": ln,
        "sums": sums,
        "muls": muls,
        "d_dx": d_dx,
        "inte": inte,
        "log": log,
        "pi": pi,
        "e": e,
        "comb": comb,
        "factorial": factorial,
        "perm": perm, 
        "pow": Pow,
        "Pow": Pow,
        "abs": abs,
        #"frac": Fraction,
        "nth_rt": nth_root,
        "gcd": gcd,
        "lcm": lcm,
        "Ran#": Ran_,
        "RandInt": Randint,
        "Int": int,
        "Rnd": Rnd,
        "Rec": Rec,
        "Pol": Pol,
        "modulo": modulo,
        "sqrt": sqrt,
        "exp": exp
    }
    if complex_choice:
        FUNC_MAP.pop("Rec")
        FUNC_MAP.pop("Pol")
        FUNC_MAP.update({
            "i": 1j,
            "ImP": ImP,
            "ReP": ReP,
            "Arg": Arg,
            "Conjg": Conjg
        })
    # Thay thế các biến đã lưu vào biểu thức
    local_dict = avail_var.copy()
    # Thêm các hằng số toán học nếu cần
    local_dict.update(actual_val_const)
    local_dict.update(vars_val)
    # Inject centralized function map so sympify/eval has access to helpers
    local_dict.update(FUNC_MAP)
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
        if not app:
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
        else: pass
    elif app:
        for s in sol:
            if s.is_real: 
                x_val = str(s)
                stor(x=x_val)
                return x_val
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
        a = n.real
        b = n.imag
        real_part = math.exp(a)
        imag_part = returning(math.cos(b)) + returning(math.sin(b)) * 1j

        return real_part * imag_part
    elif returning(n) == float("inf"):
        return float("inf")

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

_PRIMES_UP_TO_1E5 = sieve_primes(100_000)
@cache
def FACT(n: int, primes=None):
    """
    Phân tích n (n >= 1) thành các thừa số nguyên tố.
    Trả về list các tuple (prime, exponent) theo thứ tự tăng dần prime.
    Dùng tốt cho n <= 1e10 (với primes precomputed tới 1e5).
    """
    # Precompute primes up to 100000 (sufficient for n <= 1e10)
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

def customised_sqrt(n: int | float | Decimal | Fraction | complex):
    global complex_choice

    if isinstance(n, complex):
        return cmath.sqrt(n)
    elif n < 0:
        if not complex_choice: raise ValueError(MATH_ERROR)
        elif n < 0: 
            real = abs(n)
            real = returning(math.sqrt(real))
            return real*1j
    return returning(math.sqrt(n))

def cbrt(n: int | float | Decimal | Fraction | complex):
    return Pow(n, 1/3)

def nth_root(ex: float | Fraction | Decimal | int, base: float | Fraction | Decimal | int):
    return Pow(base, 1/ex)

def pow_mod(base: int, exp: int, mod: int):
    if mod == 1:
        return 0
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result


def Pow(base: int | float | Fraction | Decimal | complex,
        exp: int | float | Fraction | Decimal | complex,
        mod: int | float | Fraction | Decimal | complex | None = None):
    # MOD only allowed for integer exponent
    if mod is not None:
        if not isinstance(exp, int):
            raise TypeError("mod is only supported for integer exponent")
        if not isinstance(base, int):
            base = int(base)
        return pow_mod(base, exp, mod)
    global complex_choice
    if isinstance(exp, int):
        return returning(pow(base, exp))
    elif isinstance(exp, (float, Decimal)):
        frac = Fraction(*float.as_integer_ratio(exp)).limit_denominator()
        if base < 0:
            if frac.denominator % 2 == 0:
                if not complex_choice:
                    raise ValueError(MATH_ERROR)
                base_ = abs(base)
                res1 = pow(base_, exp)
                return res1 * 1j
            res = -pow(-base, exp)
            return returning(res)
        if base == 0:
            if exp <= 0:
                raise ValueError(MATH_ERROR)
            return 0
        #if base > 0:
        result = float(pow(base, exp))
        return returning(result)
    else:
        return pow(base, exp)
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
    #print(expression)
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
        "sin": sin, "cos": cos, "tan": tan,
        "asin": asin, "acos": acos, "atan": atan,
        "ln": ln,
        "sums": sums,
        "muls": muls,
        "d_dx": d_dx,
        "inte": inte,
        "log": log,
        "pi": pi,
        "e": e,
        "comb": comb,
        "factorial": factorial,
        "perm": perm, 
        "pow": Pow,
        "Pow": Pow,
        "abs": abs,
        #"frac": Fraction,
        "nth_rt": nth_root,
        "gcd": gcd,
        "lcm": lcm,
        "Ran#": Ran_,
        "RandInt": Randint,
        "Int": int,
        "Rnd": Rnd,
        "Rec": Rec,
        "Pol": Pol,
        "modulo": modulo,
        "sqrt": sqrt,
        "exp": exp,
    }
        if complex_choice:
            local_dict.pop("Rec")
            local_dict.pop("Pol")
            local_dict.update({
                "i": 1j,
                "ImP": ImP,
                "ReP": ReP,
                "Arg": Arg,
                "Conjg": Conjg
            })
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
    "Statistics": False,
    "Equation/ Function": False, 
    "Table": 1
}
# lst_of_stop = ["stop", "off", "exit", "quit"]
def stat_setting(choice: int = int(dict_of_setting["Statistics"])):
    global dict_of_setting
    dict_of_setting["Statistics"] = (choice == True)

    # Lấy thư mục chứa file hiện tại
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Nối đường dẫn tuyệt đối tới file muốn mở
    file_path = os.path.join(BASE_DIR, "statistics.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"{choice}")
stat_setting(0)

def eq_fu_settings(choice: int = int(dict_of_setting["Equation/ Function"])):
    global dict_of_setting

    dict_of_setting["Equation/ Function"] = (choice == True)
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
res_ = []
res_.append(str(solve_eq("x**2+B", ask=True, B=1))+"\n")
stor(x=sqrt(2)); 
res_.append(str(evaluate_expression("2x+1-3"))+"\n")
#res_.append(str(Ans) + "\n")
res_.append(str(calc("2A - 3", A=6))+"\n")
res_.append(str(returning(sqrt(2)))+"\n")
res_.append(str(d_dx("x^2 + 2x + 1", 9)) + "\n")
res_.append(str(inte(0, 4, "x^2 + 4")) + "\n")
res_.append(str(sums(0, 10, "x**2")) + "\n")
res_.append(str(muls(1, 10, "x")) + "\n")
BASE_DIR_ = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR_, "run.txt")
with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(res_)
del res_;
Ans = 0
