from decimal import Decimal, getcontext
getcontext().prec = 12  # độ chính xác toàn cục
def solve_equation_two(a1: int | float, b1: int | float, c1: int | float, 
                       a2: int | float, b2: int | float, c2: int | float, 
                       lang: int = 1) -> tuple[int | float, int | float] | str:
        if (a1 * b2 == a2 * b1 and b1 * c2 != b2 * c1):
                return "No solution!!!" if lang == 1 else "Vô nghiệm"
        elif (a1 * b2 == a2 * b1 and b1 * c2 == b2 * c1):
                return "Every Real Solution" if lang == 1 else "Vô số nghiệm"
        y = ((a2 * c1) - (a1 * c2)) / ((a2 * b1) - (a1 * b2))
        if a1 != 0:
                x = (c1 - b1 * y) / a1
        else:
                x = (c2 - b2 * y) / a2
        x = int(x) if x.is_integer() else x
        y = int(y) if y.is_integer() else y
        return (x, y)

def solve_equation_three(a1: int | float, b1: int | float, c1: int | float, k1: int | float,
                         a2: int | float, b2: int | float, c2: int | float, k2: int | float,
                         a3: int | float, b3: int | float, c3: int | float, k3: int | float, 
                         lang: int = 1) -> tuple[int | float, int | float, int | float] | str:
        D  = a1 * (b2 * c3 - b3 * c2) - b1 * (a2 * c3 - a3 * c2) + c1 * (a2 * b3 - a3 * b2)
        Dx = k1 * (b2 * c3 - b3 * c2) - b1 * (k2 * c3 - k3 * c2) + c1 * (k2 * b3 - k3 * b2)
        Dy = a1 * (k2 * c3 - k3 * c2) - k1 * (a2 * c3 - a3 * c2) + c1 * (a2 * k3 - a3 * k2)
        Dz = a1 * (b2 * k3 - b3 * k2) - b1 * (a2 * k3 - a3 * k2) + k1 * (a2 * b3 - a3 * b2)

        if D == 0:
                if Dx == Dy == Dz == 0:
                        return "Every Real Solution" if lang == 1 else "Vô số nghiệm"
                else:
                        return "No solution!!!" if lang == 1 else "Vô nghiệm"
        x = Dx / D
        y = Dy / D
        z = Dz / D
        x = int(x) if x.is_integer() else x
        y = int(y) if y.is_integer() else y
        z = int(z) if z.is_integer() else z
        return (x, y, z)
# list_of_exception = ["No solution!!!", "Vô nghiệm", "Every Real Solution", "Vô số nghiệm"]
          
#--------------input-output--------------#
if __name__ == "__main__":
        #def i_input(prompt: str):
        #        inp = input(prompt)
        #        process = eval(inp)
        #        return process
        
        lang_input = input("Select language (number):\n1. English\n2. Vietnamese\nDefault: English\n").strip()
        lang = 1 if (lang_input == "" or lang_input == "1") else 2
        INVALID_INPUT = "Invalid Input!!!" if lang == 1 else "Sai đầu vào"
        #try:
        if lang == 1:
                choice = input("How many variable: (2 / 3) \nDefault: 2\n").strip()
                if choice == "" or choice == "2":
                        print("Form: a b c")
                        inp = []
                        for _ in range(2):
                                inp.extend(list(map(eval, input().split())))
                        res = solve_equation_two(*inp, lang=lang)
                        print("Result:", sep="", end=" ")
                        if type(res) == str:
                                print(res)
                        else:
                                print(*res)
                elif choice == "3":
                        sub_choice = input("Full Form (f) or or miss equation (me)\nDefault: f\n").strip().lower()
                        if sub_choice == "f" or sub_choice == "":
                                print("Form: a b c d")
                                inp = []
                                for _ in range(3):
                                        inp.extend(list(map(eval, input().split())))
                                res = solve_equation_three(*inp, lang=lang)
                                print("Result:", sep="", end=" ")
                                if type(res) == str:
                                        print(res)
                                elif res:
                                        print(*res)
                        elif sub_choice == "me":
                                print("Form: a b c d")
                                inp = []
                                for _ in range(2):
                                        inp.extend(list(map(eval, input().split())))
                                print("Range:")
                                first = int(input("Left: "))
                                end = int(input("Right: "))
                                check = input("Z or N\nDefault: N\n").strip().upper()
                                print("Prediction: ")
                                for z in range(first, end + 1):
                                        res = solve_equation_two(inp[0], inp[1], inp[3] - inp[2]*z,
                                                                inp[4], inp[5], inp[7] - inp[6]*z, lang=lang)
                                        if type(res) == str:
                                                # print(res)
                                                continue
                                        x, y = res
                                        if first <= x <= end and first <= y <= end:
                                                if check == "Z":
                                                        if x.is_integer() and y.is_integer():
                                                                print((int(x), int(y), z))
                                                elif check == "N" or check == "":
                                                        if x.is_integer() and y.is_integer() and x >= 0 and y >= 0:
                                                                print((int(x), int(y), z))
                                                else: 
                                                        print(INVALID_INPUT)
                                                        exit(0)
                        else:
                                print(INVALID_INPUT)
        elif lang == 2:
                choice = input("Hệ phương trình bao nhiêu ẩn (2 / 3)\nMặc định: 2\n").strip()
                if choice == "" or choice == "2":
                        print("Nhập hệ số a b c (các hệ số cách nhau bằng một dấu cách)")
                        inp = []
                        for _ in range(2):
                                inp.extend(map(eval, input().split()))
                        res = solve_equation_two(*inp, lang=lang)
                        print("Kết quả:", sep="", end=" ")
                        if type(res) == str:
                                print(res)
                        else:
                                print(*res)
                elif choice == "3":
                        sub_choice = input("Đầy đủ (f) hoặc thiếu phương trình (me)\nMặc định: f\n").strip().lower()
                        if sub_choice in ["f", ""]:
                                print("Nhập hệ số a b c d (các hệ số cách nhau bằng một dấu cách)")
                                inp = []
                                for _ in range(3):
                                        inp.extend(list(map(eval, input().split())))
                                res = solve_equation_three(*inp, lang=lang)
                                print("Đáp án:", sep="", end=" ")
                                if type(res) == str:
                                        print(res)
                                else:
                                        print(*res)
                        elif sub_choice == "me":
                                print("Nhập hệ số a b c d (các hệ số cách nhau bằng một dấu cách)")
                                inp = []
                                for _ in range(2):
                                        inp.extend(list(map(eval, input().split())))
                                print("Khoảng:")
                                first = int(input("Cực tiểu: "))
                                end = int(input("Cực đại: "))
                                check = input("Tiêu chí:\nSố nguyên (Z)\nSố tự nhiên (N)\n Mặc định: N").strip().upper()
                                print("Dự đoán: ")
                                for z in range(first, end + 1):
                                        res = solve_equation_two(inp[0], inp[1], inp[3] - inp[2]*z,
                                                                inp[4], inp[5], inp[7] - inp[6]*z, lang=lang)
                                        if type(res) == str:
                                                #print(res)
                                                continue
                                        x, y = res
                                        if check == "Z":
                                                if x == int(x) and y == int(y):
                                                        print((int(x), int(y), z))
                                        elif check == "N" or "":
                                                if x == int(x) and y == int(y) and x >= 0 and y >= 0:
                                                        print((int(x), int(y), z))
                                        else: 
                                                print(INVALID_INPUT)
                                                exit(0)
                        else:
                                print(INVALID_INPUT)
        else:
                print(INVALID_INPUT)
