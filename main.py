import tkinter as tk  
import process_front_end as pfe
import process_complex as pc
returning = pfe.returning
MATH_ERROR = pfe.MATH_ERROR
complex_choice = pfe.complex_choice

TEXT_NORMAL = "black"
TEXT_ACTIVE = "#a0e000"   # vàng chữ
TEXT_ALPHA = "#db035a"    # hồng chữ

pfe.app_open(1)
SMART_TOKENS = [
        "sin(", "cos(", "tan(",
        "log(", "ln(", "sqrt(",
        "inte(", "d_dx(", "sums(", "muls(",
        "*10^", "Int(", "Pol(", "Rec(",
        "RandInt(", "pi", "Rnd(", "Ran#",
        "i", "^(", "10^", "Ans", "inf",
        "exp(", "[mod]", "_C_", "_P_",
        "nth_rt(", ")/("
] + pfe.names + list(pfe.actual_val_const)
#print(SMART_TOKENS, sep="\n")
class Calculator_fx:
        #global SHIFT_MODE, ALPHA_MODE, CALC_MODE, SOLVE_MODE
        def __init__(self):  
                self.win = tk.Tk()  
                self.win.title("Casio FX Hybrid Simulator")  
                self.win.geometry("400x600")
                self.win.config(bg="#00cbff")  
                self.win.update_idletasks()
                self.shift = False
                self.alpha = False
                self.solve_mode = False
                self.stor_mode = False
                self.watch_history = False
                self.fact_reg = "S"
                self.history = [] # ("", "", "", True) True -> có thể mở lại lịch sử... False -> tắt chế độ xem lại lịch sử
                self.history_index = -1
                self.contents = None
                self.regulation = "S"
                self.temp_value = 0
                self.extra_norm = [
                        ["OPTN", "CALC", "", "", "inte", "x"],  
                        ["frac", "sqrt", "^2", "^", "log", "ln"],  
                        ["_", "degs", "^-1", "sin", "cos", "tan"],  
                        ["Stor", "i", "(", ")", "S<=>D", "M+"]
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
                        frame, font=("monospace", 16),  
                        justify="left"  
                )  
                self.inputs.pack(fill="x", pady=2)  

                self.output = tk.Entry(  
                        frame, font=("monospace", 16),  
                        justify="right", 
                )  
                self.output.pack(fill="x", pady=2)  
        def on_press1(self, value):
                if value == "SHIFT":
                        self.shift = not self.shift
                        self.alpha = False

                elif value == "ALPHA":
                        self.alpha = not self.alpha
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
                        if self.finish_eval:
                                self.finish_eval = False # at all cost
                                self.inputs.icursor(tk.END)
                        self.output.delete(0, tk.END)
                        if pos > 0:
                                # ưu tiên di chuyển qua token dài
                                for token in sorted(SMART_TOKENS, key=len, reverse=True):
                                        L = len(token)
                                        if pos >= L and text[pos - L:pos] == token:
                                                #self.inputs.delete(pos - L, pos)
                                                self.inputs.icursor(pos - L)
                                                return
                                self.inputs.icursor(pos-1)
                        elif pos == 0:
                                if not self.inputs.get() and self.output.get():
                                        self.inputs.insert(self.history[-1][0])
                                        self.inputs.icursor(tk.END)
                                else: self.inputs.icursor(tk.END)
                elif value == "->":
                        pos = self.inputs.index(tk.INSERT)
                        self.output.delete(0, tk.END)
                        if self.finish_eval:
                                self.finish_eval = False # at all cost
                                self.inputs.icursor(0)
                        #text = self.inputs.get()
                        if pos < len(text):
                                # ưu tiên di chuyển qua token dài
                                for token in sorted(SMART_TOKENS, key=len, reverse=True):
                                        L = len(token)
                                        if text[pos:pos+L] == token:
                                                #self.inputs.delete(pos - L, pos)
                                                self.inputs.icursor(pos + L)
                                                return
                                self.inputs.icursor(pos+1)
                        elif pos == len(text):
                                if not self.inputs.get() and self.output.get():
                                        self.inputs.insert(self.history[-1][0])
                                        self.inputs.icursor(tk.END)
                                else: self.inputs.icursor(0)
                elif value == "up":
                        if self.history and (not self.inputs.get() and not self.output.get()):
                                if self.history_index == -(len(self.history)):
                                        return
                                contents = self.history[self.history_index]
                                if contents[-1]:
                                        self.history_index -= 1
                                        self.inputs.insert(0, contents[0])
                                        self.inputs.icursor(tk.END)
                                        self.output.insert(0, self.content[1])
                                        self.regulation = "S"
                        else:
                                if self.finish_eval:
                                        self.finish_eval = False
                                        self.output.delete(0, tk.END)
                                self.inputs.icursor(0)
                elif value == "down":
                        if self.history and (not self.inputs.get() and not self.output.get()):
                                if self.history_index == -1:
                                        return
                                self.contents = self.history[self.history_index]
                                self.history_index += 1
                                self.inputs.insert(0, self.content[0])
                                self.inputs.icursor(tk.END)
                                self.output.insert(0, self.content[1])
                                self.regulation = "S"
                        else:
                                if self.finish_eval:
                                        self.finish_eval = False
                                        self.output.delete(0, tk.END)
                                self.inputs.icursor(tk.END)
        def on_press3(self, value):
                """Cho bảng số hàm (frac,...)"""
                self.inputs.focus_set()
                pos = self.inputs.index(tk.INSERT)
                #print(pos)
                if value == "^":
                        if self.finish_eval:
                                self.inputs.delete(0, tk.END)
                                self.inputs.insert(0, "Ans")
                                self.output.delete(0, tk.END)
                                self.finish_eval = False
                        expr = self.inputs.get()
                        if len(expr) > 0 and pos > 0:
                                if not expr[pos-1] in ["+", "-", "*", "/", "("]:
                                        text = value+"()"
                                        self.inputs.insert(pos, value+"()")
                                        self.inputs.icursor(pos + len(text) - 1)
                        else:
                                text = text = value+"()"
                                self.inputs.insert(pos, value+"()")
                                self.inputs.icursor(pos)
                        self.output.delete(0, tk.END)
                elif value in ["^2", "^3", "^-1"]:
                        expr = self.inputs.get()
                        if self.finish_eval:
                                self.inputs.delete(0, tk.END)
                                self.inputs.insert(0, "Ans")
                                self.output.delete(0, tk.END)
                                self.finish_eval = False
                        expr = self.inputs.get()
                        expo, num = value[0], value[1:]
                        text = expo + "(" + num + ")"
                        if len(expr) > 0 and pos > 0:
                                if not expr[pos-1] in ["+", "-", "*", "/", "("]:
                                        self.inputs.insert(pos, text)
                                        self.inputs.icursor(pos + len(text))
                        else:
                                self.inputs.insert(pos, text)
                                self.inputs.icursor(pos)
                        self.output.delete(0, tk.END)
                elif value in ([",", "_", "!", "="] + pfe.names):
                        if self.finish_eval:
                                self.inputs.delete(0, tk.END)
                                #self.inputs.insert("Ans")
                                self.output.delete(0, tk.END)
                                self.finish_eval = False
                        self.inputs.insert(pos, value)
                        self.inputs.icursor(pos + len(value))
                        self.output.delete(0, tk.END)
                elif value == "(":
                        if self.finish_eval:
                                self.inputs.delete(0, tk.END)
                                #self.inputs.insert("Ans")
                                self.output.delete(0, tk.END)
                                self.finish_eval = False
                        actual_text = "(" + (")" if len(self.inputs.get()) > 0 and not self.inputs.get()[pos] else "")
                        self.inputs.insert(pos, actual_text)
                        self.inputs.icursor(pos + 1)
                elif value == ")":
                        if self.finish_eval:
                                self.inputs.delete(0, tk.END)
                                self.inputs.insert(0, ")")
                                self.output.delete(0, tk.END)
                                self.finish_eval = False
                                return
                        expr = self.inputs.get()
                        if pos == 0:
                                self.inputs.insert(pos, ")")
                                self.inputs.icursor(pos + 1)
                        elif pos < len(expr) and expr[pos] == ")":
                                self.inputs.icursor(pos + 1)
                        else:
                                self.inputs.insert(pos, ")")
                                self.inputs.icursor(pos + 1)
                        self.output.delete(0, tk.END)
                elif value == "i":
                        if pfe.complex_choice:
                                expr = self.inputs.get()
                                if pos == 0 and len(expr) == 0: pass
                                elif 0 < pos < len(expr) and expr[pos-1] in ["+", "-", "*", "/", "("]:
                                        self.inputs.insert(pos, "i")
                                        self.inputs.icursor(pos)
                                        self.output.delete(0, tk.END)
                                else:
                                        self.inputs.insert(pos, "i")
                                        self.inputs.icursor(pos+1)
                                        self.output.delete(0, tk.END)
                elif value in ["inte", "frac", "sqrt", "nth_rt", "log", "ln",
                               "sin", "cos", "tan", "asin", "acos", "atan",
                               "d_dx", "sums", "muls", "exp", "10^"]:
                        if self.finish_eval:
                                self.finish_eval = False
                                self.inputs.delete(0, tk.END)
                                self.inputs.icursor(0)
                                pos = 0
                        expr = self.inputs.get()
                        text = ("*" if (pos > 0 and (not expr[pos-1].isdigit())) else "") + value + "()"
                        self.inputs.insert(pos, text)
                        self.inputs.icursor(pos + len(text) - 1)
                        self.output.delete(0, tk.END)
                elif value == "cbrt":
                        if self.finish_eval:
                                self.finish_eval = False
                                self.inputs.delete(0, tk.END)
                                self.inputs.icursor(0)
                                pos = 0
                        expr = self.inputs.get()
                        text = ("*" if (pos > 0 and (not expr[pos-1].isdigit())) else "") + "nth_rt(3,)"
                        self.inputs.insert(pos, text)
                        self.inputs.icursor(pos + len(text) - 1)
                        self.output.delete(0, tk.END)
                elif value == "SOLVE": 
                        expr = self.inputs.get()
                        if any(i in expr for i in ["inte", "d_dx", "sums", "muls"]): 
                                self.output.delete(0, tk.END)
                                self.output.insert(0, MATH_ERROR)
                                self.finish_eval = True
                                return
                        free_symbol = []
                        for i in pfe.names:
                                if i in expr and not i == "x":
                                        free_symbol.append(i)
                        try:
                                if free_symbol:
                                        self.solve_expr = expr
                                        self.solve_vars = free_symbol
                                        self.solve_values = {}
                                        self.solve_index = 0

                                        self.inputs.delete(0, tk.END)
                                        self.output.delete(0, tk.END)
                                        self.inputs.insert(0, f"{free_symbol[0]}=")
                                else:
                                        self.output.delete(0, tk.END)
                                        sol = pfe.solve_eq(expr)
                                        if isinstance(sol, list) and len(sol) == 0:
                                                self.output.insert(0, "No solution.")
                                                self.solve_mode = False
                                        self.output.insert(0, sol)
                        except: self

                elif value == "Abs":
                        if self.finish_eval:
                                self.inputs.delete(0, tk.END)
                                #self.inputs.insert("Ans")
                                self.output.delete(0, tk.END)
                                self.finish_eval = False
                        self.inputs.insert(pos, "||")
                        self.inputs.icursor(pos+1)
                elif value == "[mod]":
                        if self.finish_eval:
                                self.inputs.delete(0, tk.END)
                                #self.inputs.insert("Ans")
                                self.output.delete(0, tk.END)
                                self.finish_eval = False
                        self.inputs.insert(pos, "[mod]")
                        self.inputs.icursor(pos+len("[mod]"))
                elif value == "OPTN":
                        pass
                elif value == "CALC":
                        expr = self.inputs.get()
                        free_symbol = []
                        for i in pfe.names:
                                if i in expr:
                                        free_symbol.append(i)
                        if free_symbol:
                                self.calc_mode = True
                                self.calc_ing = True
                                self.calc_expr = expr
                                self.calc_vars = free_symbol
                                self.calc_values = {}
                                self.calc_index = 0

                                self.inputs.delete(0, tk.END)
                                self.output.delete(0, tk.END)
                                self.inputs.insert(0, f"{free_symbol[0]}=")
                        else:
                                try:
                                        res = pfe.evaluate_expression(expr)
                                        self.output.delete(0, tk.END)
                                        self.output.insert(0, str(res))
                                        self.regulation = "S"
                                        self.finish_eval = True
                                except Exception as ex:
                                        self.output.delete(0, tk.END)
                                        self.output.insert(0, ex)
                                        self.finish_eval = True
                elif value == "S<=>D" and self.history:
                        self.output.delete(0, tk.END)
                        if self.regulation == "S":
                                self.output.insert(0, self.history[self.history_index][2])
                                self.regulation = "D"
                        else:
                                self.history[self.history_index][1]
                                self.regulation = "S"
                elif value == "FACT": 
                        number = self.output.get()
                        try:
                                number = int(number)
                                if self.fact_reg == "S":
                                        number = int(number)
                                        if number >= 1e10: return
                                        facts = pfe.FACT(number)
                                        text = ""
                                        for i, pair in enumerate(facts):
                                                if i == 0:
                                                        ba, ex = pair
                                                        text += f"{ba}^({ex})"
                                                        continue
                                                ba, ex = pair
                                                text += f"*{ba}^({ex})"
                                        self.output.delete(0, tk.END)
                                        self.output.insert(0, text)
                                        self.fact_reg = "N"
                                else: 
                                        facts_str = self.output.get()
                                        number = pfe.evaluate_expression(facts_str)
                                        self.output.delete(0, tk.END)
                                        self.output.insert(0, str(number))
                                        self.fact_reg = "S"
                        except: pass
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
                self.inputs.focus_set()
                pos = self.inputs.index(tk.INSERT)
                """Cho bảng số"""
                if value == "AC":
                        self.finish_eval = False
                        self.inputs.delete(0, tk.END)
                        self.output.delete(0, tk.END)
                elif value == "DEL":
                        self.finish_eval = False
                        text = self.inputs.get()
                        del_right = False
                        if pos == 0:
                                del_right = True
                        # ưu tiên xoá token dài
                        for token in sorted(SMART_TOKENS, key=len, reverse=True):
                                L = len(token)
                                #print(text[pos - L:pos], token)
                                if pos >= L and text[pos - L:pos] == token:
                                        self.inputs.delete(pos - L, pos)
                                        self.inputs.icursor(pos - L)
                                        return
                                elif del_right and text[pos:pos + L] == token:
                                        self.inputs.delete(pos, pos + L)
                                        self.inputs.icursor(pos)
                                        return
                        # fallback: xoá 1 ký tự
                        if del_right:
                                self.inputs.delete(pos, pos+1)
                                self.inputs.icursor(pos)
                        else:
                                self.inputs.delete(pos - 1, pos)
                                self.inputs.icursor(pos - 1)
                        self.output.delete(0, tk.END)
                elif value == "=":
                        self.output.delete(0, tk.END)
                        if not self.calc_mode:
                                try:
                                        expr = self.inputs.get()
                                        if "=" in expr:
                                                self.output.insert(0, MATH_ERROR)
                                                self.finish_eval = True
                                                return
                                        result = pfe.evaluate_expression(expr)
                                        if isinstance(result, tuple):
                                                if result[-1] == "mod":
                                                        self.output.insert(0, f"{result[0]}, R={result[1]}")
                                                elif result[-1] == "pol":
                                                        self.output.insert(0, f"r={result[0]}, {pfe.theta_symbol}={result[1]}")
                                                elif result[-1] == "rec":
                                                        self.output.insert(0, f"x={result[0]}, y={result[1]}")
                                        elif isinstance(result, complex):
                                                if complex_choice:
                                                        self.output.insert(0, pc.format_complex_output(str(result)))
                                                else:
                                                        self.output.insert(0, str(result))
                                        else:
                                                self.regulation = "S"
                                                self.fact_reg = "S"
                                                self.finish_eval = True
                                                self.output.insert(0, str(result))
                                                self.history.append((expr, result, pfe.returning(result, "D"), True))
                                except Exception as ex:
                                        self.output.delete(0, tk.END)
                                        self.output.insert(0, ex)
                                        self.finish_eval = True
                                        self.history.append((expr, False))


                elif value == "OFF":
                        exit(0)
                elif value in ["Int", "Pol", "Rnd", "RandInt", "Rec"]:
                        if self.finish_eval or self.calc_ing:
                                self.inputs.delete(0, tk.END)
                                self.output.delete(0, tk.END)
                                self.finish_eval = False
                        text = value + "()"
                        self.inputs.insert(pos, text)
                        self.inputs.icursor(pos+len(text)-1)
                elif value in "+-*/":
                        if self.finish_eval:
                                self.inputs.delete(0, tk.END)
                                self.finish_eval = False
                                self.output.delete(0, tk.END)
                                self.inputs.insert(0, "Ans" + value)
                                self.inputs.icursor(tk.END)
                                return

                        self.inputs.insert(pos, value)
                        self.inputs.icursor(pos+1)
                elif value in [str(i) for i in range(10)]:
                        if self.finish_eval:
                                self.inputs.delete(0, tk.END)
                                self.finish_eval = False
                                self.calc_ing = False
                                self.output.delete(0, tk.END)
                                self.inputs.insert(0, value)
                                self.inputs.icursor(tk.END)
                                return
                        self.inputs.insert(pos, value)
                        self.inputs.icursor(pos+1)
                elif value == "nCr":
                        if self.finish_eval:
                                self.inputs.delete(0, tk.END)
                                self.finish_eval = False
                                self.output.delete(0, tk.END)
                                self.inputs.insert(0, "Ans_C_")
                                self.inputs.icursor(len("Ans_C_"))
                        else:
                                self.inputs.insert(pos, "_C_")
                                self.inputs.icursor(pos+3)
                elif value == "nPr":
                        if self.finish_eval:
                                self.inputs.delete(0, tk.END)
                                self.finish_eval = False
                                self.output.delete(0, tk.END)
                                self.inputs.insert(0, "Ans_P_")
                                self.inputs.icursor(len("Ans_P_"))
                        else:
                                self.inputs.insert(pos, "_P_")
                                self.inputs.icursor(pos+3)
                elif value == "CONST":
                        pass
                elif value == "CONV":
                        pass
                elif value == "INS":
                        pass
                else:
                        self.output.delete(0, tk.END)
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
                btn.config(bg="#00cbff")

                arrows = ["<-", "", "->"]  
                for i, a in enumerate(arrows):  
                        btn = tk.Button(
                                frame, text=a,
                                width=2, height=1,
                                takefocus=0,
                                state="disabled" if a == "" else "normal"
                        )
                        btn.grid(row=1, column=i, padx=2)
                        btn.config(bg="#00cbff")
                        if a:
                                btn.bind("<Button-1>", lambda e, t=a: self.on_press2(t))

                btn = tk.Button(frame, text="down", width=2, height=1)
                btn.grid(row=2, column=1, pady=2)
                btn.bind("<Button-1>", lambda e: self.on_press2("down"))
                btn.config(bg="#00cbff")
        def build_extra_grid(self):  
                self.extra_frame = tk.Frame(self.win)
                self.extra_frame.pack(pady=4)
                #self.extra_color = TEXT_NORMAL

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
                                if self.shift:
                                        self.extra_color = TEXT_ACTIVE
                                elif self.alpha:
                                        self.extra_color = TEXT_ALPHA
                                else:
                                        self.extra_color = TEXT_NORMAL
                                btn.config(fg=self.extra_color, bg="#00cbff")
        def build_main_grid(self):  
                self.main_frame = tk.Frame(self.win)
                self.main_frame.pack(pady=6)
                #self.main_color = TEXT_NORMAL
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
                                if self.shift:
                                        self.main_color = TEXT_ACTIVE
                                elif self.alpha:
                                        self.main_color = TEXT_ALPHA
                                else:
                                        self.main_color = TEXT_NORMAL
                                btn.config(fg=self.main_color, bg="#00cbff")
        def run(self):  
                self.win.mainloop()  

Calculator_fx().run()
