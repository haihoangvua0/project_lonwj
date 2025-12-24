import tkinter as tk

class Calculator_fx:
        def __init__(self):
                self.win = tk.Tk()
                self.win.title("Casio FX Hybrid Simulator")
                self.win.geometry("430x620")
                self.win.update_idletasks()
                print("Window width:", self.win.winfo_width())
                print("Window height:", self.win.winfo_height())
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
                        justify="right"
                )
                self.output.pack(fill="x", pady=2)
        
        def build_top_keys(self):
                frame = tk.Frame(self.win)
                frame.pack(pady=4)

                for i, txt in enumerate(["SHIFT", "ALPHA", "MODE", "OFF"]):
                        tk.Button(
                                frame, text=txt,
                                width=9, height=2
                        ).grid(row=0, column=i, padx=3)

        def build_extra_grid(self):
                frame = tk.Frame(self.win)
                frame.pack(pady=4)

                grid = [
                        ["OPTN", "CALC", "inte", "x"],
                        ["frac", "sqrt", "^2", "^", "log", "ln"],
                        ["_", "degs", "^-1", "sin", "cos", "tan"],
                        ["Stor", "[Empty]", "(", ")", "S<=>D", "M+"]
                ]

                for r, row in enumerate(grid):
                        for c, txt in enumerate(row):
                                tk.Button(
                                        frame, text=txt,
                                        width=7, height=2
                                ).grid(row=r, column=c, padx=2, pady=2)

        def build_replay(self):
                frame = tk.Frame(self.win)
                frame.pack(pady=4)

                tk.Button(frame, text="up", width=6, height=2).grid(row=0, column=1, pady=2)

                arrows = ["<-", "", "->"]
                for i, a in enumerate(arrows):
                        tk.Button(
                                frame, text=a,
                                width=6, height=2,
                                state="disabled" if a == "" else "normal"
                        ).grid(row=1, column=i, padx=2)
                tk.Button(frame, text="down", width=6, height=2).grid(row=2, column=1, pady=2)
        
        def build_main_grid(self):
                frame = tk.Frame(self.win)
                frame.pack(pady=6)

                grid = [
                        ["7", "8", "9", "DEL", "AC"],
                        ["4", "5", "6", "*", "/"],
                        ["1", "2", "3", "+", "-"],
                        ["0", ".", "*10**", "Ans", "="],
                ]

                for r, row in enumerate(grid):
                        for c, txt in enumerate(row):
                                tk.Button(
                                        frame, text=txt,
                                        width=6, height=2
                                ).grid(row=r, column=c, padx=2, pady=2)
        
        def run(self):
                self.win.mainloop()

Calculator_fx().run()
