import tkinter as tk  
from process_front_end import *

#COLOR_NORMAL = "#f0f0f0"
#COLOR_SHIFT = "#ffeeba"   # vàng nhạt
#COLOR_ALPHA = "#ee8fff"   # hồng nhạt

TEXT_NORMAL = "black"
TEXT_ACTIVE = "#d39e00"   # vàng chữ
TEXT_ALPHA = "#c2185b"    # hồng chữ

app_open(1)
SMART_TOKENS = [
        "sin(", "cos(", "tan(",
        "log(", "ln(", "sqrt(",
        "inte(", "frac(",
        "d_dx(", "sums(", "muls(",
        "*10^", "Int(", "Pol(", "Rec(",
        "RandInt(", "pi", "Rnd(", "Ran#",
        
]
class Calculator_fx:  
        #global SHIFT_MODE, ALPHA_MODE, CALC_MODE, SOLVE_MODE
        def __init__(self):  
                self.win = tk.Tk()  
                self.win.title("Casio FX Hybrid Simulator")  
                self.win.geometry("400x600")
                self.win.config(bg="#B0E0E6")  
                self.win.update_idletasks()
                self.shift = False
                self.alpha = False
                self.calc_mode = False
                self.calc_ing = False
                self.solve_mode = False
                self.stor_mode = False
                self.history = [
                        ("", "", False)
                ] # ("", "", True) True -> có thể mở lại lịch sử... False -> tắt chế độ xem lại lịch sử
                self.regulation = "S"
                self.temp_value = 0
                self.extra_norm = [
                        ["OPTN", "CALC", "", "", "inte", "x"],  
                        ["frac", "sqrt", "^2", "^", "log", "ln"],  
                        ["_", "degs", "^-1", "sin", "cos", "tan"],  
                        ["Stor", "j", "(", ")", "S<=>D", "M+"]
                ]
                self.extra_alpha = [
                        ["", "=", "", "", "", "muls"],
                        ["[mod]", "", "", "", "", ""],
                        ["A", "B", "C", "D", "E", "F"],
                        ["", "", "x", "y", "z", "M"]
                ]
                self.extra_shift = [
                        ["", "SOLVE", "", "", "d_dx", "sums"],
                        ["", "cbrt", "^3", "nth_rt", "10^", "exp"],
                        ["", "FACT", "!", "asin", "acos", "atan"],
                        ["RECALL", "", "Abs", ",", "", "M-"]
                ]
                self.main_norm = [
                        ["7", "8", "9", "DEL", "AC"],  
                        ["4", "5", "6", "*", "/"],  
                        ["1", "2", "3", "+", "-"],  
                        ["0", ".", "*10^", "Ans", "="]
                ]
                self.main_shift = [
                        ["CONST", "CONV", "RESET", "INS", "OFF"],
                        ["", "", "", "nPr", "nCr"],
                        ["", "", "", "Pol", "Rec"],
                        ["Rnd", "Ran#", "pi", "%", ""]
                ]
                self.main_alpha = [
                        ["", "", "", "", ""],
                        ["", "", "", "gcd", "lcm"],
                        ["", "", "", "Int", ""],
                        ["", "RandInt", "e", "", ""]
                ]
                self.base_n = ["DEC", "BIN", "HEX", "OCT"]
                # Dựng máy.
                self.build_display()
                self.build_top_keys()
                self.build_replay()
                self.build_extra_grid()
                self.build_main_grid() 
        def build_display(self):  
                frame = tk.Frame(self.win)  
                frame.pack(fill="x", padx=6, pady=4)  

                self.inputs = tk.Entry(  
                        frame, font=("Cascadia Mono", 16),  
                        justify="left"  
                )  
                self.inputs.pack(fill="x", pady=2)  

                self.output = tk.Entry(  
                        frame, font=("Cascadia Mono", 16),  
                        justify="right", 
                )  
                self.output.pack(fill="x", pady=2)  
        def on_press1(self, value):
                if value == "SHIFT":
                        self.shift = not self.shift
                        self.main_color = TEXT_ACTIVE if self.shift else TEXT_NORMAL
                        self.extra_color = TEXT_ACTIVE if self.shift else TEXT_NORMAL
                        self.alpha = False
            
                elif value == "ALPHA":
                        self.alpha = not self.alpha
                        self.main_color = TEXT_ALPHA if self.alpha else TEXT_NORMAL
                        self.main_color = TEXT_ALPHA if self.alpha else TEXT_NORMAL
                        self.shift = False
            
                elif value == "MODE":
                        pass
            
                elif value == "SETUP":
                        pass
            
                elif value == "ON":
                        self.inputs.delete(0, tk.END)
                        self.output.delete(0, tk.END)
            
                    # rebuild UI khi đổi mode
                self.extra_frame.destroy()
                self.main_frame.destroy()
                self.build_extra_grid()
                self.build_main_grid()

        def on_press2(self, value):
                """Cho 4 nút điều hướng"""
                self.inputs.focus_set()
                pos = self.inputs.index(tk.INSERT)
                text = self.inputs.get()
                if value == "<-":
                        if pos > 0:
                                self.inputs.icursor(pos - 1)
                        elif pos == 0 and not self.inputs.get(): pass
                        elif pos == 0:
                                self.inputs.icursor(tk.END)
                elif value == "->":
                        if pos < len(text):
                                self.inputs.icursor(pos + 1)
                        elif pos == len(text):
                                if not self.inputs.get(): pass
                                else:
                                        self.inputs.icursor(0)
                elif value == "up":
                        #if self.history and not self.inputs.get():
#                                expr, res, flag = self.history[-1]
#                                if flag:
#                                        self.inputs.delete(0, tk.END)
#                                        self.inputs.insert(0, expr)
#                                        self.output.delete(0, tk.END)
#                                        self.output.insert(0, res)
                        pass

                elif value == "down":
                        # Sau này mở rộng replay nhiều bước
                        pass
        def on_press3(self, value):
                """Cho bảng số hàm (frac,...)"""
                self.inputs.focus_set()
                pos = self.inputs.index(tk.INSERT)
                #print(pos)
                if value in ["^-1", "^2", "^3", "^"]:
                        expr = self.inputs.get()
                        if not expr[pos-1] in ["+", "-", "*", "/", "("]:
                                self.inputs.insert(pos, value)
                                self.inputs.icursor(pos + len(value))
                        else:
                                self.inputs.insert(pos, value)
                                self.inputs.icursor(pos)
                        self.output.delete(0, tk.END)
                elif value in ([",", "_"] + names):
                        self.inputs.insert(pos, value)
                        self.inputs.icursor(pos + 1)
                        self.output.delete(0, tk.END)
                elif value == "(":
                        self.inputs.insert(pos, "()")
                        self.inputs.icursor(pos + 1)
                elif value == ")":
                        expr = self.inputs.get()
                        if pos == 0:
                                self.inputs.insert(pos, ")")
                                self.inputs.icursor(pos + 1)
                        elif expr[pos-1] == ")":
                                self.inputs.icursor(pos + 1)
                        else:
                                self.inputs.insert(pos, ")")
                                self.inputs.icursor(pos + 1)
                        self.output.delete(0, tk.END)
                elif value == "j":
                        if complex_choice:
                                self.inputs.insert(pos, "*1j")
                                self.inputs.icursor(pos + 3)
                                self.output.delete(0, tk.END)
                elif value in ["inte", "frac", "sqrt", "log", "ln", "sin", "cos", "tan",
                                "d_dx", "sums", "muls"]:
                        text = value+"()"
                        self.inputs.insert(pos, text)
                        self.inputs.icursor(pos + len(text) - 1)
                        self.output.delete(0, tk.END)
                elif value == "OPTN":
                        pass
                elif value == "CALC":
                        expr = self.inputs.get()
                        free_symbol = []
                        for i in names:
                                if i in expr:
                                        free_symbol.append(i)
                        if free_symbol:
                                self.calc_mode = True
                                self.calc_expr = expr
                                self.calc_vars = free_symbol
                                self.calc_values = {}
                                self.calc_index = 0

                                self.inputs.delete(0, tk.END)
                                self.output.delete(0, tk.END)
                                self.inputs.insert(0, f"{free_symbol[0]}=")
                        else:
                                try:
                                        res = evaluate_expression(expr)
                                        self.output.delete(0, tk.END)
                                        self.output.insert(0, str(res))
                                except:
                                        self.output.delete(0, tk.END)
                                        self.output.insert(0, MATH_ERROR)
                elif value == "S<=>D":
                        expr = self.inputs.get()
                        res = evaluate_expression(expr)
                        self.temp_value = res
                        self.output.delete(0, tk.END)
                        if self.regulation == "S":
                                self.output.insert(0, returning(res, "D"))
                                self.regulation = "D"
                        else:
                                self.output.insert(0, self.temp_value)
                                self.regulation = "S"
                if self.shift:
                        self.shift = False
                        self.extra_frame.destroy()
                        self.main_frame.destroy()
                        self.build_extra_grid()
                        self.build_main_grid()
                elif self.alpha:
                        self.alpha = False
                        self.extra_frame.destroy()
                        self.main_frame.destroy()
                        self.build_extra_grid()
                        self.build_main_grid()
        def on_press4(self, value):
                #global SHIFT_MODE, ALPHA_MODE, CALC_MODE, SOLVE_MODE
                """Cho bảng số"""
                if value == "AC":
                        self.inputs.delete(0, tk.END)
                        self.output.delete(0, tk.END)
                elif value == "DEL":
                        self.inputs.focus_set()
                        pos = self.inputs.index(tk.INSERT)
                        if pos > 0:
                                self.inputs.delete(pos - 1, pos)
                                self.inputs.icursor(pos - 1)
                        elif pos == 0:
                                if len(self.inputs.get()) == 0:
                                        pass # Do nothing
                                else:
                                        self.inputs.delete(pos, pos + 1)
                        self.output.delete(0, tk.END)
                elif value == "=":
                        if not self.calc_mode:
                                try:
                                        expr = self.inputs.get()
                                        result = evaluate_expression(expr)
                                        self.output.delete(0, tk.END)
                                        self.output.insert(0, str(result))
                                except:
                                        self.output.delete(0, tk.END)
                                        self.output.insert(0, MATH_ERROR)
                        else:
                                try:
                                        current_var = self.calc_vars[self.calc_index]
                                        val = evaluate_expression(self.inputs.get().split("=")[1])
                                        self.calc_values[current_var] = val

                                        self.calc_index += 1

                                        # Còn biến tiếp
                                        if self.calc_index < len(self.calc_vars):
                                                self.inputs.delete(0, tk.END)
                                                self.inputs.insert(0, f"{self.calc_vars[self.calc_index]}=")
                                        else:
                                        # Tính xong
                                                res = calc(expr=self.calc_expr, **self.calc_values)
                                                self.output.delete(0, tk.END)
                                                self.output.insert(0, str(res))

                                                self.inputs.delete(0, tk.END)
                                                self.inputs.insert(0, self.calc_expr)

                                                self.calc_mode = False
                                except:
                                        self.output.delete(0, tk.END)
                                        self.output.insert(0, MATH_ERROR)
                elif value == "OFF":
                        exit(0)
                else:
                        self.output.delete(0, tk.END)
                        # ép Entry lấy lại focus# ép Entry lấy lại focus
                        self.inputs.focus_set()

                        # lấy vị trí cursor HIỆN TẠI
                        pos = self.inputs.index(tk.INSERT)

                        # chèn text trước cursor
                        self.inputs.insert(pos, value)

                        # đưa cursor tới sau ký tự vừa chèn
                        self.inputs.icursor(pos + len(value))
                if self.shift:
                        self.shift = False
                        self.extra_frame.destroy()
                        self.main_frame.destroy()
                        self.build_extra_grid()
                        self.build_main_grid()
                elif self.alpha:
                        self.alpha = False
                        self.extra_frame.destroy()
                        self.main_frame.destroy()
                        self.build_extra_grid()
                        self.build_main_grid()
        def build_top_keys(self):  
                frame = tk.Frame(self.win)  
                frame.pack(pady=4)  
                for i, txt in enumerate(["SHIFT", "ALPHA", "MODE", "ON"]):
                        btn = tk.Button(
                                frame, text=txt,
                                width=4, height=1,
                                takefocus=0
                        )
                        btn.grid(row=0, column=i, padx=3)
                        btn.bind("<Button-1>", lambda e, t=txt: self.on_press1(t))
        def build_replay(self):  
                frame = tk.Frame(self.win)  
                frame.pack(pady=4)
            
                btn = tk.Button(frame, text="up", width=2, height=1)
                btn.grid(row=0, column=1, pady=2)
                btn.bind("<Button-1>", lambda e: self.on_press2("up"))
            
                arrows = ["<-", "", "->"]  
                for i, a in enumerate(arrows):  
                        btn = tk.Button(
                                frame, text=a,
                                width=2, height=1,
                                takefocus=0,
                                state="disabled" if a == "" else "normal"
                        )
                        btn.grid(row=1, column=i, padx=2)
                        if a:
                                btn.bind("<Button-1>", lambda e, t=a: self.on_press2(t))
            
                btn = tk.Button(frame, text="down", width=2, height=1)
                btn.grid(row=2, column=1, pady=2)
                btn.bind("<Button-1>", lambda e: self.on_press2("down"))
        def build_extra_grid(self):  
                self.extra_frame = tk.Frame(self.win)
                self.extra_frame.pack(pady=4)
                self.extra_color = TEXT_NORMAL
            
                if self.shift:
                        grid = self.extra_shift
                elif self.alpha:
                        grid = self.extra_alpha
                else:
                        grid = self.extra_norm
            
                for r in range(len(grid)):  
                        for c in range(len(grid[0])):
                                txt = grid[r][c]
                                btn = tk.Button(
                                        self.extra_frame,
                                        text=txt,
                                        width=2, height=2,
                                        state="disabled" if txt == "" else "normal",
                                        takefocus=0
                                )
                                btn.grid(row=r, column=c, padx=2, pady=2)
                                btn.bind("<Button-1>", lambda e, t=txt: self.on_press3(t))
                                btn.config(fg=self.extra_color)
        def build_main_grid(self):  
                self.main_frame = tk.Frame(self.win)
                self.main_frame.pack(pady=6)
                self.main_color = TEXT_NORMAL
                if self.shift:
                        grid = self.main_shift
                elif self.alpha:
                        grid = self.main_alpha
                else:
                        grid = self.main_norm
                for r, row in enumerate(grid):  
                        for c, txt in enumerate(row):  
                                btn = tk.Button(
                                        self.main_frame,
                                        text=txt,
                                        width=4,
                                        height=3,
                                        takefocus=0
                                )
                                btn.grid(row=r, column=c, padx=2, pady=2)
                                btn.bind("<Button-1>", lambda e, t=txt: self.on_press4(t))
                                btn.config(fg=self.main_color)
        def run(self):  
                self.win.mainloop()  

Calculator_fx().run()