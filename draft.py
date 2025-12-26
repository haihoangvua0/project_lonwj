import tkinter as tk  
from process_front_end import *
# Trong process_front_end có các hàm như inte,... và có 3 hàm đặc biệt evaluate_expression, solve_eq, calc

SHIFT_MODE = False
ALPHA_MODE = False
CALC_MODE = False
SOLVE_MODE = False
#ITER_MODE = False
class Calculator_fx:  
        #global SHIFT_MODE, ALPHA_MODE, CALC_MODE, SOLVE_MODE
        def __init__(self):  
                self.win = tk.Tk()  
                self.win.title("Casio FX Hybrid Simulator")  
                self.win.geometry("400x600")  
                self.win.update_idletasks()  
                #print("Window width:", self.win.winfo_width())  
                #print("Window height:", self.win.winfo_height())  
                self.win.attributes("-topmost", True)
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
                """Cho 4 nút công cụ"""
                pass
        def on_press2(self, value):
                """Cho 4 nút điều hướng"""
                pass
        def on_press3(self, value):
                global SHIFT_MODE, ALPHA_MODE, CALC_MODE, SOLVE_MODE
                """Cho bảng số hàm (frac,...)"""
                pos = self.inputs.index(tk.INSERT)
                if value in ([",", "_", "x", "^-1", "^", "^2", "^3", "(", ")"] + names):
                        self.inputs.insert(pos, value)
                elif value == "j":
                        if complex_choice:
                                self.inputs.insert(pos, "*1j")
                elif value in ["inte", "frac", "sqrt", "log", "ln", "sin", "cos", "tan",
                               "d_dx", "sums", "muls"]:
                        self.inputs.insert(pos, value+"(")
                elif value == "OPTN":
                        pass
                elif value == "CALC":
                        expr = self.inputs.get()
                        free_symbol = []
                        for i in names:
                                if i in expr:
                                        free_symbol.append(i)
                        if free_symbol:
                                CALC_MODE = True
                                dict_of_res = {}
                                self.inputs.delete(0, tk.END)
                                self.output.delete(0, tk.END)
                                for i in free_symbol:
                                        self.inputs.insert(f"{i}=")
                                        # Đến đây thì muốn cho số vào output, xong sau khi bấm dấu bằng rồi cho vào dict có sẵn rồi gán nguyên hàm calc vào...
                                        self.inputs.delete(0, tk.END)
                                self.inputs.delete(0, tk.END)
                                self.output.delete(0, tk.END)
                                self.inputs.insert(0, expr)
                                self.output.insert(0, f"{calc(expr=expr, **dict_of_res)}")
                        else:
                                self.output.delete(0, tk.END)
                                self.output.insert(0, f"{evaluate_expression(expr)}")
        def on_press4(self, value):
                global SHIFT_MODE, ALPHA_MODE, CALC_MODE, SOLVE_MODE
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
                        self.output.delete(0, tk.END)
                elif value == "=":
                        try:
                                expr = self.inputs.get()
                                result = evaluate_expression(expr)
                                self.output.delete(0, tk.END)
                                self.output.insert(0, str(result))
                        except:
                                self.output.delete(0, tk.END)
                                self.output.insert(0, MATH_ERROR)
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
        def build_top_keys(self):  
                frame = tk.Frame(self.win)  
                frame.pack(pady=4)  
  
                #self.win.update_idletasks()  
  
                for i, txt in enumerate(["SHIFT", "ALPHA", "MODE", "OFF"]):  
                        tk.Button(  
                                frame, text=txt,  
                                width=4, height=1  
                        ).grid(row=0, column=i, padx=3)  
  
        def build_extra_grid(self):  
                frame = tk.Frame(self.win)  
                frame.pack(pady=4)  
  
                grid = [  
                        ["OPTN", "CALC", "", "", "inte", "x"],  
                        ["frac", "sqrt", "^2", "^", "log", "ln"],  
                        ["_", "degs", "^-1", "sin", "cos", "tan"],  
                        ["Stor", "j", "(", ")", "S<=>D", "M+"]  
                ]  
  
                #self.win.update_idletasks()  
  
                for r in range(len(grid)):  
                        for c in range(len(grid[0])):
                                txt = grid[r][c]
                                tk.Button(  
                                        frame, text=txt,  
                                        width=2, height=2,  
                                        state="disabled" if txt == "" else "normal" 
                                ).grid(row=r, column=c, padx=2, pady=2)  
  
        def build_replay(self):  
                frame = tk.Frame(self.win)  
                frame.pack(pady=4)  
  
                #self.win.update_idletasks()  
  
                tk.Button(frame, text="up", width=2, height=1).grid(row=0, column=1, pady=2)  
  
                arrows = ["<-", "", "->"]  
                for i, a in enumerate(arrows):  
                        tk.Button(  
                                frame, text=a,  
                                width=2, height=1,
                                takefocus=0,
                                state="disabled" if a == "" else "normal"  
                        ).grid(row=1, column=i, padx=2)  
  
                tk.Button(frame, text="down", width=2, height=1).grid(row=2, column=1, pady=2)  
  
        def build_main_grid(self):  
                frame = tk.Frame(self.win)  
                frame.pack(pady=6)  
  
                grid = [  
                        ["7", "8", "9", "DEL", "AC"],  
                        ["4", "5", "6", "*", "/"],  
                        ["1", "2", "3", "+", "-"],  
                        ["0", ".", "*10^", "Ans", "="],  
                ]  
  
                for r, row in enumerate(grid):  
                        for c, txt in enumerate(row):  
                                btn = tk.Button(
                                        frame,
                                        text=txt,
                                        width=4,
                                        height=3,
                                        takefocus=0
                                )
                                btn.grid(row=r, column=c, padx=2, pady=2)
                                
                                btn.bind("<Button-1>", lambda e, t=txt: self.on_press4(t))
                                
  
        def run(self):  
                self.win.mainloop()  
  
Calculator_fx().run()
