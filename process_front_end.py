""" Backend module for FX-580 simulator (functions collected & refined) """

# Module needed for all
from functools import cache
import math, cmath, random, os
from decimal import Decimal, getcontext
from fractions import Fraction
from decimal import Decimal
getcontext().prec = 50
# Symbol
theta_symbol = "\u03B8"     
pi_symbol = "\u03C0"        
degree = "\u00B0"    
angle = "\u2220"     
sqrt_symbol = "\u221A"
analyze_deg = "\u25FB"
radian_deg = "\u02B3"
gradian_deg = "\u1D4D"

# Default vars needed
Randint = random.randint
Ran_ = random.random()
Rnd = round

MATH_ERROR = "MATH ERROR"
gcd = math.gcd
lcm = math.lcm

# 1. Numeric primitives

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

class Pi:
    def __init__(self, coef = 1, out = 0) -> None:
        self.val = coef * math.pi + out
        self.coef = coef
        self.add = out
    @property
    def value(self): return self.val
    def __str__(self) -> str:
        display = ""
        if self.coef == 1:
            display += f"{pi_symbol}"
        elif self.coef == -1:
            display += f"-{pi_symbol}"
        else:
            if self.coef:
                display += f"{self.coef}{pi_symbol}"
            else: return "0"

        if self.add > 0:
            return "(" + display + f"+{self.add})"
        elif self.add < 0:
            return "(" + display + f"{self.add})"
        else:
            return display if display else "0"
    def __repr__(self) -> str:
        return self.__str__()
    def __add__(self, other):
        if isinstance(other, Pi):
            return Pi(self.coef + other.coef, self.add + other.add)
        return Pi(self.coef, self.add + other)
    def __radd__(self, other):
        return self + other
    def __sub__(self, other):
        return self - other
    def __rsub__(self, other):
        return -self + other
    def __mul__(self, other):
        if isinstance(other, REAL):
            return Pi(self.coef * other, self.add * other)
        if isinstance(other, (complex, Complex)):
            return Complex(other.real * self, other.imag * self)
    def __rmul__(self, other):
        return self * other
    def __truediv__(self, other):
        if isinstance(other, Pi): return self.value / other.value
        return Pi(self.coef / other, self.add / other)
    def __rtruediv__(self, other):
        return other / self.value
    def __pow__(self, other):
        if other == 0:
            return 1
        if other == 1:
            return self
        if other not in {0, 1}:
            return self.value ** other
    def __rpow__(self, other):
        return other ** self.value
    def __neg__(self):
        return (-1) * self
    def __abs__(self):
        return ((-1) if self < 0 else 1) * self
    def __eq__(self, value: object) -> bool:
        return self.val == value
    def __ne__(self, value: object) -> bool:
        return not self == value
    def __lt__(self, other) -> bool:
        return self.value < other
    def __le__(self, other) -> bool:
        return self.value <= other
    def __gt__(self, other) -> bool:
        return self.value > other
    def __ge__(self, other) -> bool:
        return self.value >= other
    def __format__(self, format_spec: str) -> str:
        return format(self.value, format_spec)
    def __int__(self): return int(self.value)
    def __float__(self): return self.value

pi = Pi()

# 2. Complex mode state
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

# 3. Square-root helpers
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

# 4. Square-root and complex types
class sqrt:
    def __init__(self, n: int | float | list | Fraction | Decimal | complex):
        self.val = None

        # mặc định
        self.coef = None
        self.radicand = None
        self.sums_terms = None
        # itself:
        if isinstance(n, sqrt):
            self.coef = customised_sqrt(n.value)
            self.radicand = 1
        # ===== REAL =====
        elif isinstance(n, (int, float, Fraction, Decimal, Pi)):
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
                self.coef = out * i
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
            terms = 0
            for i in items_self:
                for j in items_other:
                    out = i[0] * j[0]
                    ins = i[1] * j[1]
                    outside, inside = split_in_out(ins)
                    terms += sqrt([(outside*out, inside)])
            return terms
        elif isinstance(other, (int, float, Fraction, Decimal, Complex)):
            if isinstance(other, (int, float, Fraction, Decimal)):
                if other == 1: return self
                if check_irrational(other): pass
                else: other = Fraction(*float(other).as_integer_ratio()).limit_denominator()
            elif isinstance(other, Complex):
                return NotImplemented
            else: return NotImplemented
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
            if 2 <= (other) <= 5:
                res = 1
                for _ in range(other):
                    res *= self
                return res
            elif other == 0: return 1
            elif other == 1: return self
            elif other < 0: return 1/(self**abs(other))
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
    def __neg__(self):
        return (-1)*self

# 5. Runtime values
REAL = (int, float, Fraction, Decimal, euler_num, sqrt)
class Complex:
    def __init__(self, real: int | float | Fraction | Decimal = 0, 
                       imag: int | float | Fraction | Decimal = 0):
        self.re = None
        self.im = None
        # real part
        if isinstance(real, (complex, Complex)):
            self.re = returning(real.real)
            self.im = returning(real.imag)
        elif isinstance(real, REAL + (Pi,)):
            self.re = returning(real)
        else: raise ValueError(f"Initialization Error for \"{real = }\"")
        # imaginary part
        if isinstance(imag, (complex, Complex)): 
            re = returning(imag.real)
            im = returning(imag.imag)
            # A + (a+bi)i = (A - b) + ai
            if self.re is not None \
               and self.im is not None:
                self.re -= im
                self.im += re
                # final modify
        elif isinstance(imag, REAL):
            imag = returning(imag)
            self.im = imag
        else: raise ValueError(f"Initialization Error for \"{imag = }\"")
    # Class properties and attributes
    @property
    def real(self): return self.re
    @property
    def imag(self): return self.im
    def conjugate(self): return Complex(self.real, -self.imag)
    # Built-in method
    def __str__(self):
        display = ""
        # real part
        if self.re == 0: pass
        else: display += str(self.re)
        # imaginary part
        if self.im == 0: pass
        elif self.im == 1: display += ("+" if (display) else "") + "i"
        elif self.im == -1: display += "-i"
        elif isinstance(self.im, sqrt):
            if len(self.im.items) > 1:
                if self.im > 0:
                    if display: text = f'+({self.im})'
                    else: text = f'({self.im})'
                else:
                    text = f"-({abs(self.im)})"
            else:
                if self.im > 0:
                    if display: text = f'+{self.im}'
                    else: text = f'{self.im}'
                else:
                    text = f"-{abs(self.im)}"
            display += (text + "i")
        elif isinstance(self.im, Fraction): display += (("+" if (self.im > 0 and display) else "") + f"({self.im})") + 'i'
        else: display += (("+" if (self.im > 0 and display) else "") + str(self.im)) + 'i'
        # process output
        if display == "":
            return "0"
        else:
            return display
    def __repr__(self):
        return str(self)
    def __add__(self, other):
        if isinstance(other, REAL):
            real = self.real
            real += other
            return Complex(real, self.imag)
        if isinstance(other, (complex, Complex)):
            real = self.real + returning(other.real)
            imaginary = self.imag + returning(other.imag)
            return Complex(real, imaginary)
        return NotImplemented
    def __radd__(self, other):
        return self + other
    def __sub__(self, other):
        return self + (-1)*other
    def __rsub__(self, other):
        return (-1)*self + other
    def __mul__(self, other):
        if isinstance(other, (complex, Complex)):
            real = self.real*returning(other.real) - self.imag*returning(other.imag)
            imaginary = self.real*returning(other.imag) + self.imag*returning(other.real)
            return Complex(real, imaginary)
        if isinstance(other, REAL):
            return Complex(returning(self.real * other), returning(self.imag * other))
        return NotImplemented
    def __rmul__(self, other):
        return self * other
    def __truediv__(self, other):
        if isinstance(other, REAL):
            return Complex(returning(self.real / other), returning(self.imag / other))
        if isinstance(other, (complex, Complex)):
            numerator = self * other.conjugate()
            denominator = (other.real)**2 + (other.imag)**2
            # return to the form z / c, as z is complex and c is real
            return numerator / denominator
        return NotImplemented
    def __rtruediv__(self, other):
        numerator = other * self.conjugate()
        denominator = (self.real)**2 + (self.imag)**2
        return numerator / denominator
    def __pow__(self, other):

        # ----- INTEGER POWER -----
        if isinstance(other, int):
            if other == 0:
                return Complex(1, 0)
            if other < 0:
                return Complex(1,0) / (self ** (-other))

            result = Complex(1, 0)
            base = self
            while other:
                if other & 1:
                    result *= base
                base *= base
                other >>= 1
            return result


        # ----- REAL POWER -----
        if isinstance(other, (int, float, Fraction, Decimal)):

            r, theta = Pol(self.real, self.imag)

            new_r = r ** other
            new_theta = theta * other

            x, y = Rec(new_r, new_theta)
            return Complex(x, y)


        # ----- COMPLEX POWER -----
        if isinstance(other, (complex, Complex)):

            a = other.real
            b = other.imag

            r, theta = Pol(self.real, self.imag)

            if r == 0:
                return Complex(0,0)

            log_r = log(r)

            exp_real = math.exp(a * log_r - b * theta)
            new_theta = a * theta + b * log_r

            x, y = Rec(exp_real, new_theta)
            return Complex(x, y)

        return NotImplemented
    def __rpow__(self, other):
        if isinstance(other, REAL):
            return Complex(other, 0) ** self
        if isinstance(other, complex):
            return Complex(other.real, other.imag) ** self
        return NotImplemented
    def __format__(self, format_spec):
        return format(str(self), format_spec)

# 6. Constants and persisted state
e = euler_num()

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
    #print(variable)
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
    global Ans
    stor_ = Ans
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Nối đường dẫn tuyệt đối tới file muốn mở
    file_path = os.path.join(BASE_DIR, "ans.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(stor_))
#stor_ans()

def open_ans():
    global Ans
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Nối đường dẫn tuyệt đối tới file muốn mở
    file_path = os.path.join(BASE_DIR, "ans.txt")

    with open(file_path, "r", encoding="utf-8") as f:
        Ans = f.readlines()[-1]
        Ans = evaluate_expression(Ans)

# 7. Constants and angle mode
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
# 8. Angle mode and trig
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

# 9. Shared math helpers
def convert_deg(x: int | float | Fraction | Decimal):
    if ANGLE_MODE == "DEG":
        return returning(math.degrees(x))
    if ANGLE_MODE == "GRA":
        return returning(x * 200 / pi)
    return returning(x)   # RAD
# 3. Trig functions (Casio-compatible) + Hypebolic Funcs
def sin(x):
    a = _to_radian_if_needed(x)

    # bẫy bội của pi
    k = round(a / pi)
    if abs(a - k * pi) <= 1e-12:
        return 0

    beta = returning((180 * a) / pi)

    base = {
        0: 0,
        15: Fraction(1,4)*(sqrt(6) - sqrt(2)),
        18: Fraction(1,4)*(sqrt(5) - 1),
        30: Fraction(1,2),
        45: Fraction(1,2)*sqrt(2),
        60: Fraction(1,2)*sqrt(3),
        75: Fraction(1,4)*(sqrt(6) + sqrt(2)),
        90: 1
    }

    if beta <= 90:
        return base.get(beta, returning(math.sin(a)))
    if beta <= 180:
        return base.get(180 - beta, returning(math.sin(a)))
    if beta <= 270:
        return -base.get(beta - 180, returning(math.sin(a)))
    return -base.get(360 - beta, returning(math.sin(a)))

def cos(x):
    global ANGLE_MODE
    if ANGLE_MODE == "DEG":
        return sin(90 - x)
    elif ANGLE_MODE == "RAD":
        return sin(pi/2 - x)
    elif ANGLE_MODE == "GRA":
        return sin(100 - x)

def tan(x):
    c = cos(x)
    if c == 0:
        return float('inf')
    return sin(x) / c

def asin(x: float):
    v = math.asin(x)
    return convert_deg(v)

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
# 10. Core helpers

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

class scientific_number(float):
    def __new__(cls, value: float):
        value = float(value)
        obj = float.__new__(cls, value)
        if value == 0 or math.isinf(value) or math.isnan(value):
            obj.a = value
            obj.k = 0
            return obj

        formatted = f"{value:.12e}"
        base_text, exp_text = formatted.split("e")
        base_value = float(base_text)
        mantissa = round(base_value, 9)
        if abs(mantissa - round(mantissa)) < 1e-12:
            obj.a = int(round(mantissa))
        else:
            obj.a = float(f"{mantissa:.9f}".rstrip("0").rstrip("."))
        obj.k = int(exp_text)
        return obj

    def _mantissa_text(self) -> str:
        if isinstance(self.a, int):
            return str(self.a)

        mantissa = float(self.a)
        if abs(mantissa - round(mantissa)) < 1e-12:
            return str(int(round(mantissa)))

        return f"{mantissa:.9f}".rstrip("0").rstrip(".")

    def __str__(self):
        if self.a == 0:
            return "0"
        if self.k == 0:
            return self._mantissa_text()
        return f"{self._mantissa_text()}*10^({self.k})"

    def __repr__(self):
        return str(self)

    def __format__(self, format_spec):
        return format(str(self), format_spec)

def abs(n: int | float | Fraction | Decimal | complex | Complex):
    if isinstance(n, REAL + (Pi,)):
        if isinstance(n, (float, Decimal)):
            n = float(n)
        return (-1)*n if n < 0 else n
    if isinstance(n, (complex, Complex)): return sqrt((n.real)**2 + (n.imag)**2)
    raise TypeError(f"Not Implemented for {type(n) = }")

# ---------------------------------------------------------
# 11. Unified returning
# ---------------------------------------------------------

class returning:
    """Normalize numeric results while preserving the original call style."""

    def __new__(cls, n: int | float | Decimal | sqrt | complex | Pi,
                choice: str = "S",
                /):
        global complex_choice

        if isinstance(n, Decimal):
            n = float(n)

        if isinstance(n, float) and (math.isnan(n) or math.isinf(n)):
            return float("inf")

        if isinstance(n, (int, float)):
            if abs(n) < 1e-100:
                return 0

            n = float(n)
            if n != 0 and (abs(n) <= 1e-10 or abs(n) >= 1e10):
                return scientific_number(n)

            if abs(n - round(n)) < 1e-8:
                return int(round(n))

        elif isinstance(n, complex):
            if not complex_choice:
                raise ValueError(MATH_ERROR)
            return n
        elif isinstance(n, sqrt):
            if choice == "D":
                return n.value
            if choice == "S":
                return n
        elif isinstance(n, euler_num):
            return n.value
        elif isinstance(n, Pi):
            return n if choice.upper() == "S" else n.value

        if check_irrational(n):
            new_n = f"{n:.12f}".rstrip("0").rstrip(".")
            actual1 = float(new_n)
            if abs(actual1 - round(actual1)) < 1e-20:
                return int(round(actual1))
            if actual1 != 0 and (abs(actual1) <= 1e-10 or abs(actual1) >= 1e10):
                return scientific_number(actual1)
            return actual1
        if isinstance(n, scientific_number):
            return n

        if choice.upper() == "S":

            frac = Fraction(*float(n).as_integer_ratio()).limit_denominator()
            if abs(float(frac) - n) < 1e-15:
                if frac.denominator == 1:
                    return frac.numerator
                return frac


        s = f"{n:.12f}".rstrip("0").rstrip(".")
        actual = float(s)
        if abs(actual - round(actual)) < 1e-12:
            return int(round(actual))

        if actual != 0 and (abs(actual) <= 1e-10 or abs(actual) >= 1e10):
            return scientific_number(actual)

        return actual

def check_irrational(n: float) -> bool:
    try:
        from fractions import Fraction
        f = Fraction(n).limit_denominator()
        return abs(float(f) - n) > 1e-50
    except Exception:
        return True

# =========================
# Polar / rectangular helpers
def Pol(x: int | float | Fraction | Decimal, y: int | Fraction | float | Decimal, ask: bool = False):
    r = returning(math.hypot(x, y))
    theta = returning(convert_deg(math.atan2(y, x)))
    if ask:
        return r, theta, "pol"
    elif complex_choice:
        return r, theta
    return r

def Rec(r: int | float | Fraction | Decimal, theta: int | float | Fraction | Decimal, ask: bool = False):
    theta = _to_radian_if_needed(theta)
    x = returning(r * math.cos(theta))
    y = returning(r * math.sin(theta))
    if ask:
        return x, y, "rec"
    elif complex_choice:
        return x, y
    return returning(x)

# =========================
# Complex process helpers
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
                return 0
        else:
            return 0
    else: return 0

def Conjg(z: int | float | Fraction | complex):
    if complex_choice:
        if isinstance(z, (complex, Complex)):
            return z.conjugate()
        else:
            raise TypeError(MATH_ERROR)
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

def insert(index: int, string: str, sub_string: str):
    """Insert sub_string into BEFORE the index of string"""
    before = string[:index]#; print(before)
    after = string[index:]#; print(after)
    new = before + sub_string + after
    return new
# 12. Expression engine
def preprocess_expression(expr: str, *, form=False) -> str: 
    global names 
    import re  

    #expr = expr.replace("^", "**")  
    expr = expr.strip(" ")
    if "÷÷" in expr:
        raise ValueError("Syntax ERROR")
    elif "**" in expr:
        if not form: raise ValueError("Syntax ERROR")
        expr = expr.replace("**", "^")
        #print(expr)
        # start to iter
        i = 0
        while i < len(expr):
            if expr[i] == "^":
                if i < len(expr) - 1 and expr[i+1] == "(":
                    pass
                else:
                    # find the exponent
                    start = i + 1
                    for j in range(start, len(expr)):
                        if expr[j] in "+-*/÷×":
                            break
                    stop = j+1 if j < len(expr) - 1 else None
                    #print(i, j, len(expr))
                    #print(expr)
                    expr = insert(start, expr, "(")
                    if stop == None:
                        stop = len(expr)
                    expr = insert(stop, expr, ")")
                    print(expr)
                    i += (stop - start + 2)
                    continue
            i += 1
    expr = expr.replace("÷", "/")
    #expr = expr.replace("×", "*")
    # -------------------------------  
    # protect expression argument in inte()  
    # inte(a,b,expr)  -> inte(a,b,"expr")  
    # -------------------------------  
    def add_close_parentheses(expr: str):
        from collections import Counter
        list_of_parentheses = []
        for i in expr:
            if i == "(" or ')': list_of_parentheses.append(i)
        if len(list_of_parentheses) == 0: return expr
        if list_of_parentheses[0] == ")": raise ValueError(MATH_ERROR)
        count = Counter(list_of_parentheses)
        if count["("] > count[")"]:
            text = expr + (")" * (count["("] - count[")"]))
            return text
        elif count["("] == count[")"]:
            return expr
        else: raise ValueError(MATH_ERROR)
    expr = add_close_parentheses(expr)

    def repl_inte(m):  
        expr, low, high = m.groups()  
        return f'inte("{expr}",{low},{high})'  

    expr = re.sub(  
        r'inte\(\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^)]*)\s*\)',  
        repl_inte,  
        expr  
    )  
    def repl_sigma(m):  
        expr, low, high = m.groups()  
        return f'sums("{expr}",{low},{high})'  

    expr = re.sub(  
        r'sums\(\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^)]*)\s*\)',  
        repl_sigma,  
        expr  
    )  
    def repl_muls(m):  
        expr, low, high = m.groups()  
        return f'muls("{expr}",{low},{high})'   

    expr = re.sub(  
        r'muls\(\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^)]*)\s*\)',  
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
    # power ^()
    # -------------------------------  
    funcs = [  
        "sqrt", "sin", "cos", "tan", "asin", "acos", "atan",  
        "log", "ln", "exp", "sums", "muls", "inte",  
        "nth_rt", "pow", "Pow", "abs", "factorial", "gcd", "lcm",  
        "modulo"  
    ]
    str_of_func = "|".join(funcs)
    new = names + [pi_symbol, "e", "Ans", "MatA", "MatB", "MatC", "MatD"] + list(actual_val_const)
    str_of_var = "|".join(new)
    func_calls = []  
    def protect_func(m):  
        func_calls.append(m.group(0))  
        return f"__FUNC{len(func_calls)-1}__"  

    expr = re.sub(  
        rf'({str_of_func})+\([^()]*\)',  
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
    # As func is protected -> ...
    expr = parse_power(expr)
    #expr = add_close_parentheses(expr) # if needed
    # -------------------------------  
    # protect scientific notation  
    # -------------------------------  
    #sci_pattern = re.compile(r'\d+(?:\.\d+)?e[+-]?\d+')  
    #sci_tokens = []  
    #expr = sci_pattern.sub(  
    #    lambda m: f"__SCI{sci_tokens.append(m.group(0)) or len(sci_tokens)-1}__",  
    #    expr  
    #)  

    # restore func
    for i, f in enumerate(func_calls):  
        expr = expr.replace(f"__FUNC{i}__", f) 
    # -------------------------------  
    # implicit multiplication  
    # -------------------------------   
    expr = re.sub(r'(\d)\(', r'\1*(', expr)  
    expr = re.sub(r'\)\(', ')*(', expr)
    expr = re.sub(rf'\)({str_of_var})', r')*\1', expr)  
    #expr = re.sub(r'(\d)([A-Za-z])', r'\1*\2', expr) 
    expr = re.sub(rf'(\d)({str_of_func})', r'\1*\2', expr) 
    expr = re.sub(rf'({str_of_var})({str_of_var})', r'\1*\2', expr)  # biến với biến
    expr = re.sub(rf"({str_of_var})({str_of_func})", r'\1*\2', expr) # biến với hàm
    expr = re.sub(rf"({str_of_var})(\d)", r"\1*\2", expr)
    expr = re.sub(rf"(\d)({str_of_var}|VecA|VecB|VecC|VecD)", r"\1*\2", expr)
    #expr = expr.replace("e*xp", "exp")
    expr = expr.replace("int*e", "inte")
    expr = expr.replace("nt*h_rt", "nth_rt")
    # -------------------------------  
    # restore scientific notation  
    # -------------------------------  
    #for i, val in enumerate(sci_tokens):  
    #    expr = expr.replace(f"__SCI{i}__", val)
    return expr

def evaluate_expression(expr: str,
                        *,
                        simplify_symbolic=True,
                        from_=False):
    global variable, A, B, C, D, E, F, x, y, z, M, names, Ans, app
    expr_clean = preprocess_expression(expr, form=from_)
    #print(expr_clean)
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
        "exp": exp,
        "inf": float("inf"),
        pi_symbol: pi
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
        "i": i
    } if complex_choice else {}))
    avail_vars = {k: v for k, v in zip(names, variable)}
    new_ |= avail_vars
    safe |= new_
    res = eval(expr_clean, {"__builtins__": {}}, safe)
    if isinstance(res, (tuple, list, dict, str, set, range)): return res
    res = returning(res)
    Ans = res
    return res

def solve_eq(expr: str, var='x', *, ask: bool = False, **vars_val):
    #try:
        global A, B, C, D, E, F, x, y, z, M, actual_val_const, Ans  
        from sympy import sympify, Eq, Symbol, solve  

        # Nếu không có dấu "=", coi là =0  
        if "=" not in expr:  
            expr = expr + "=0"  

        left, right = expr.split("=")  
        left = preprocess_expression(left); right = preprocess_expression(right)  
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
                "i": i,  
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
                        res.append(Complex(re_f, im_f))  
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
    #except:
#        pass

# 13. Roots and powers
def exp(n: int | float | Decimal | Fraction | sqrt | complex):
    global complex_choice, ANGLE_MODE
    if isinstance(n, complex):
        if not complex_choice:
            raise ValueError(MATH_ERROR)
        a = n.real
        b = n.imag
        real_part = math.exp(a)
        imag_part = returning(math.cos(b)) + returning(math.sin(b)) * i

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
    if isinstance(n, (sqrt, float, Decimal)): return []
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
            return real*i
    return returning(math.sqrt(n))

def cbrt(n: int | float | Decimal | Fraction | complex):
    return Pow(n, 1/3)

def nth_root(ex: float | Fraction | Decimal | int, base: float | Fraction | Decimal | int):
    if ex == 2: return sqrt(ex)
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


# 14. Combinatorics
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
        if frac == 0.5: return sqrt(base)
        if base < 0:
            if frac.denominator % 2 == 0:
                if not complex_choice:
                    raise ValueError(MATH_ERROR)
                base_ = abs(base)
                res1 = pow(base_, exp)
                return res1 * i
            res = -pow(-base, exp)
            return returning(res)
        if base == 0:
            if exp <= 0:
                raise ValueError(MATH_ERROR)
            return 0
        #if base > 0:
        result = float(pow(base, exp))
        return returning(result)
    elif returning(exp) == 0.5: return sqrt(base)
    else:
        return pow(base, exp)

# 15. Differentials + log
def log(*args):

    if len(args) == 1:
        base = 10
        num = args[0]
    elif len(args) == 2:
        base, num = args
    else:
        raise TypeError("log() takes 1 or 2 arguments")

    # ----- COMPLEX -----
    if isinstance(num, (complex, Complex)):

        r, theta = Pol(num.real, num.imag)

        if r == 0:
            raise ValueError("math domain error")

        ln_r = math.log(float(r))
        ln_base = math.log(float(base))

        real_part = ln_r / ln_base
        imag_part = theta / ln_base

        return Complex(returning(real_part),
                       returning(imag_part))

    # ----- REAL -----
    return returning(math.log(num, base))
def ln(num):
    if not isinstance(num, (complex, Complex)):
        if num == 0:
            return float('-inf')

    return log(math.e, num)

def lim(point, expr, *, direction="both",
        steps=30, base=10,
        INF=1e4):
    """
    direction: "left", "right", "both"
    """

    def eval_at(x):
        return calc(expr, **{"x": x}, stor_in=False)
    try:
        return eval_at(point)
    except:
        pass
    def scan(sign):
        last = None
        for k in range(1, steps + 1):
            dx = base ** (-k)
            x = point + sign * dx
            try:
                val = eval_at(x)
            except:
                continue

            if abs(val) >= INF:
                return float("inf") if val > 0 else float("-inf")

            if last is not None:
                if abs(val) > abs(last) and abs(val) > 1e6:
                    last = val
                else:
                    return val
            else:
                last = val
        return last

    left = right = None

    if direction in ("left", "both"):
        left = scan(-1)
    if direction in ("right", "both"):
        right = scan(+1)

    if left is None and right is None:
        raise ValueError("Undefined limit")

    if left is None:
        return right
    if right is None:
        return left

    if left == right:
        return left

    raise ValueError("Two-sided limit does not exist")

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
                return evaluate_expression(str(res), from_=True) 
        except Exception as er:
            raise ValueError("Error message:" + er)
def inte(expression: str, low: float, high: float, *, var: str = "x"):
    from sympy import symbols, integrate, sympify
    global actual_val_const
    x = symbols(var)
    #print(expression)
    expr = sympify(preprocess_expression(expression), )
    #print(expr)
    try:
        res = (integrate(expr, (x, low, high)))
        #print(res)
        if res.is_real:
            return returning(res)
        else: # if isinstance(res, str):
            return evaluate_expression(str(res), from_=True)
    except:
        res = integrate(expr, x)
        new_primitive = str(res)
        print(new_primitive)
        return calc(new_primitive, stor_in=False, x=high) - calc(new_primitive, stor_in=False, x=low)

# 16. Series / product helpers
def sums(expression: str, first: int, end: int, *, var: str = "x"):
    from sympy import symbols, summation, sympify
    i = symbols(var)
    expr = sympify(preprocess_expression(expression))
    res = (summation(expr, (i, first, end)))
    #print(str(res))
    if res.is_real:
        return returning(res)
    else: # if isinstance(res, str):
        return evaluate_expression(str(res), from_=True)

def muls(expression: str, first: int, end: int, *, var: str = "x"):
    from sympy import symbols, product, sympify
    i = symbols(var)
    expr = sympify(preprocess_expression(expression))
    res = (product(expr, (i, first, end)))
    if res.is_real:
        return returning(res)
    else: # if isinstance(res, str):
        return evaluate_expression(str(res), from_=True)

# 17. Expression calculation
def calc(expr: str, stor_in=True, **vars_values):
    from sympy import sympify
    expr = preprocess_expression(expr)

    # Tách các biến từ chuỗi
    symbols = list(sympify(expr).free_symbols)
    symbols = list(map(str, symbols))
    if 'e' in symbols:
        symbols.remove('e')
    #print(symbols)
    global actual_val_const, A, B, C, D, E, F, x, y, z, M, complex_choice
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

        avail_var |= vars_values
        if stor_in:
            stor(**avail_var)
            return evaluate_expression(expr)
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
            "exp": exp,
            "inf": float("inf")
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
            "i": i
        } if complex_choice else {}))
        new_ |= avail_var
        safe |= new_
        res = eval(expr, {"__builtins__": {}}, safe)
        if isinstance(res, (tuple, list, dict, str, set, range)): return res
        res = returning(res)
        Ans = res
        return res

# 18. Runtime state and persistence
app = False
variable = [0 for _ in range(10)]
A, B, C, D, E, F, x, y, z, M = variable
names = ["A", "B", "C", "D", "E", "F", "x", "y", "z", "M"]
Ans = 0

def rcl():
    global variable

    # Lấy thư mục chứa file hiện tại
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Nối đường dẫn tuyệt đối tới file muốn mở
    file_path = os.path.join(BASE_DIR, "variable.txt")

    with open(file_path, "r", encoding="utf-8") as f:
        variable = list(map(returning, map(evaluate_expression, f.read().splitlines())))
rcl()

# 19. Settings store/load
dict_of_setting = {
    "Angle unit": ANGLE_MODE,
    "Statistics": False,
    "Equation/ Function": False, 
    "Table": 1
}

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

# 20. Self-test / smoke test
i = Complex(0, 1)
stor_settings()
res_ = []
res_.append(str(solve_eq("x^(2)+B", ask=True, B=1))+"\n")
stor(x=sqrt(2)); 
res_.append(str(evaluate_expression("2x+1-3"))+"\n")
res_.append(str(Ans) + "\n")
res_.append(str(calc("2A - 3", A=6))+"\n")
res_.append(str(returning(sqrt(2)))+"\n")
res_.append(str(d_dx("x^(2) + 2x + 1", 9)) + "\n")
res_.append(str(inte("x^(2) + 4", 0, 4)) + "\n")
res_.append(str(sums("x^(2)", 0, 10)) + "\n")
res_.append(str(muls("x", 1, 10)) + "\n")
BASE_DIR_ = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR_, "run.txt")
with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(res_)
del res_;
Ans = 0

if __name__ == "__main__":
    print(sin(75))