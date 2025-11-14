from process_front_end import *
import cmath
# 2-power
# Phương trình bậc nhất.
  
def solve_1(a: float, b: float):
        return -b/a
  
# Phương trình bậc 2
  
def solve_2(a: int | float, b: int | float, c: int | float, choice: bool):
        if a == 0:
                return solve_1(b, c)
        delta = b**2 - 4*a*c
        if delta > 0:
                return [returning((-b + sqrt(delta))/(2 * a)), returning((-b - sqrt(delta))/(2 * a))]
        elif delta == 0:
                x = -b / (2*a)
                return [returning(x)]
        else:
                if choice == True:
                        real_part = -b / (2*a)
                        imag_part = math.sqrt(-delta) / (2*a)
                        x1 = complex(real_part, imag_part)
                        x2 = complex(real_part, -imag_part)
                        return [x1, x2]
  
                elif choice == False:
                        return "No Solution!!!"  
# 3-power
def solve_3(a: float, b: float, c: float, d: float, choice: bool):
    if a == 0:
        # Nếu a = 0 thì quay lại bậc 2
        return solve_2(b, c, d, choice)

    # Chuyển về dạng thu gọn: x = t - b/(3a)
    p = (3*a*c - b**2) / (3 * a**2)
    q = (2*b**3 - 9*a*b*c + 27*a**2*d) / (27 * a**3)
    delta = (q/2)**2 + (p/3)**3

    # Căn bậc 3 an toàn cho cả số âm / phức
    def cbrt(z):
        if isinstance(z, complex):
            return z ** (1/3)
        return z ** (1/3) if z >= 0 else -(-z) ** (1/3)

    # Tính nghiệm
    if delta > 0:
        # Một nghiệm thực, hai nghiệm phức
        if choice:
            u = cbrt(-q/2 + cmath.sqrt(delta))
            v = cbrt(-q/2 - cmath.sqrt(delta))
            t1 = u + v
            t2 = -(u + v)/2 + (u - v)*cmath.sqrt(3)*1j/2
            t3 = -(u + v)/2 - (u - v)*cmath.sqrt(3)*1j/2
            roots = (t1 - b/(3*a), t2 - b/(3*a), t3 - b/(3*a))
        else:
            u = cbrt(-q/2 + math.sqrt(delta))
            v = cbrt(-q/2 - math.sqrt(delta))
            t1 = u + v
            roots = (returning(t1 - b/(3*a)),)
    elif abs(delta) < 1e-12:
        # Ba nghiệm thực, có nghiệm kép
        u = cbrt(-q/2)
        x1 = 2*u - b/(3*a)
        x2 = -u - b/(3*a)
        roots = (returning(x1), returning(x2))
    else:
        # Ba nghiệm thực phân biệt
        phi = math.acos(-q/(2*math.sqrt(-(p/3)**3)))
        t1 = 2*math.sqrt(-p/3)*math.cos(phi/3)
        t2 = 2*math.sqrt(-p/3)*math.cos((phi + 2*math.pi)/3)
        t3 = 2*math.sqrt(-p/3)*math.cos((phi + 4*math.pi)/3)
        roots = (returning(t1 - b/(3*a)), returning(t2 - b/(3*a)), returning(t3 - b/(3*a)))

    return roots
# 4-power
def solve_4(a: int | float, b: int | float, c: int | float, d: int | float, f: int | float):
        pass
if __name__ == "__main__":
                print("#=#=#=# Polynomial Equation tester #=#=#=#")
                first_choice = int(input("Input degree?\nSelect 2 to 4\n").strip())
        #try:
                if first_choice == 2:
                        a, b, c = map(int, input("a b c\n").split())
                        cmplx = int(input("Complex Result?\n1: On\n0: Off\n"))
                        try:
                                if cmplx == 1:
                                        cmplx = True
                                else:
                                        cmplx = False
                        except: cmplx = False
                        result = solve_2(a, b, c, cmplx)
                        print("Result: ", end=" ")
                        if isinstance(result, str): print(result)
                        else: print(*result[:2])
                elif first_choice == 3:
                        a, b, c, d = map(int, input("a b c d\n").split())
                        cmplx = int(input("Complex Result?\n1: On\n0: Off\n"))
                        try:
                                if cmplx == 1:
                                        cmplx = True
                                else:
                                        cmplx = False
                        except: cmplx = False
                        result = solve_3(a, b, c, d, cmplx)
                        print("Result: ", end=" ")
                        if isinstance(result, str): print(result)
                        else: print(*result[:3])
                elif first_choice == 4:
                        #a, b, c, d, f = map(int, input("a b c").split())
                        #cmplx = int(input("Complex Result?\n1: On\n0: Off"))
                        #try:
                        #        if cmplx == 1:
                        #                cmplx = True
                        #        else:
                        #                cmplx = False
                        #except: cmplx = False
                        #print("Result: ", *solve(a, b, c, cmplx))
                        print("In progess...")
        #except:
                #print("E@$#R!!!")