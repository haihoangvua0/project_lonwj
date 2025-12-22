from process_front_end import *
# 2-power
# Phương trình bậc nhất.
eq_fu_settings(1)
cmplx = dict_of_setting["Equation/ Function"] 

def solve_1(a: float, b: float):
        if a == 0:
                raise ValueError(MATH_ERROR)
        return returning(-b/a)
  
# Phương trình bậc 2
  
def solve_2(a: int | float, b: int | float, c: int | float):
        if a == 0:
                return solve_1(b, c)
        delta = b**2 - 4*a*c
        solved = []
        if delta > 0:
                solved.append([returning((-b + sqrt(delta))/(2 * a)), returning((-b - sqrt(delta))/(2 * a))])
        elif delta == 0:
                x = -b / (2*a)
                solved.extend([returning(x)])
        else:
                if cmplx == True:
                        real_part = -b / (2*a)
                        imag_part = math.sqrt(-delta) / (2*a)
                        x1 = complex(real_part, imag_part)
                        x2 = complex(real_part, -imag_part)
                        solved.append([x1, x2])
                else:
                        solved.append("No solution.")
        # Cực điểm (đỉnh):
        designated_point = [returning(-b/2*a), returning(-delta/4*a)]
        l_h = "Lowest Point" if a > 0 else "Highest Point"
        solved.append((designated_point, l_h))
        return solved

# 3-power
def solve_3(a: int | float | Fraction,
            b: int | float | Fraction,
            c: int | float | Fraction,
            d: int | float | Fraction
):
        global cmplx
        if a == 0:
                return solve_2(b, c, d)
        expr = f"{a}*x**3+{b}*x**2+{c}*x+{d}"
        res = solve_eq(expr, ask=True)
        if not cmplx == False:
                res = [i for i in res if not isinstance(i, complex)]
                if not res:
                        res.append("No solution(s)")
        d_f = d_dx(expr)
        delta_ = b**2-3*a*c
        if delta_ <= 0:
                res.append("No extreme(s)")
                return res
        else: # delta_ > 0
                sols = solve_eq(d_f, ask=True)
                o_res = [(tep := sols[0], calc(expr, x=tep)), (tep1 := sols[1], calc(expr, x=tep1))]
                o_res.sort(key=lambda x: x[1])
                extremes = [("Local min", o_res[0]),
                             ("Local max", o_res[1])
                ]
                res += extremes
                return res

def solve_4(a: int | float | Fraction,
            b: int | float | Fraction,
            c: int | float | Fraction,
            d: int | float | Fraction,
            fr: int | float | Fraction
):
        if a == 0:
                return solve_3(b, c, d, fr)
        expr = f"{a}*x**4+{b}*x**3+{c}*x**2+{d}*x+{fr}"
        res = solve_eq(expr, ask=True)
        if not cmplx:
                res = [i for i in res if not isinstance(i, complex)]
                if not res:
                        return "No solution"
                return res
        return res
if __name__ == "__main__":
        print("#=#=#=# Polynomial Equation tester #=#=#=#")
        first_choice = int(input("Input degree?\nSelect 2 to 4\n").strip())
        try:
                if first_choice == 2:
                        a, b, c = map(evaluate_expression, input("a b c\n").split())
                        result = solve_2(a, b, c)
                        print("Result: ", end=" ")
                        if isinstance(result[0], str): print(result)
                        else: print(*result)
                elif first_choice == 3:
                        inp = []
                        print("Input a b c d:", sep="")
                        while len(inp) < 4:
                                inp.extend(map(int, input().split()))
                        a, b, c, d = inp
                        result = solve_3(a, b, c, d)
                        print("Result: ", end=" ")
                        if isinstance(result, str): print(result)
                        else: print(*result)
                elif first_choice == 4:
                        inp = []
                        print("Input a b c d e:", sep="")
                        while len(inp) < 5:
                                inp.extend(map(int, input().split()))
                        a, b, c, d, fr = inp
                        result = solve_4(a, b, c, d, fr)
                        print("Result:", *result)
        except:
                print("E@R#R!!!")
