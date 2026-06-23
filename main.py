"""File-App 1: Calculator Casio FX-580 mode Calculate"""
import tkinter as tk  
import process_front_end as pfe
from collections import deque
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
        "Int(", "Pol(", "Rec(",
        "RandInt(", "Rnd(", "Ran#",
        "^(", "Ans",
        "exp(", "[mod]", "_C_", "_P_",
        "nth_rt("
] + pfe.names + list(pfe.actual_val_const)

def patch_entry_cursor(entry: tk.Entry):
        original_icursor = entry.icursor

        def icursor_with_ensure(index):
                original_icursor(index)
                try:
                        entry.update_idletasks()
                        # Tự động đồng bộ khung nhìn theo vị trí con trỏ thực tế
                        idx = entry.index(tk.INSERT)
                        total = max(len(entry.get()), 1)
                        entry.xview_moveto(max(0.0, (idx - 5) / total)) # Chừa khoảng trống nhỏ phía trước để dễ nhìn
                except Exception:
                        pass

        entry.icursor = icursor_with_ensure

class Calculator_fx:
        def __init__(self):  
                self.win = tk.Tk()  
                self.win.title("Casio FX Hybrid Simulator")  
                self.win.geometry("600x800")
                self.win.config(bg="#00cbff")  
                self.win.update_idletasks()
                self.shift = False
                self.alpha = False
                self.eval_state = "eval" 
                self.fact_reg = "S"
                self.history = deque() # Lưu trữ tuple kết quả
                self.current = ""
                self.history_index = -1 # Sửa lại mặc định -1 (chưa duyệt history)
                self.finish_eval = False
                self.regulation = "S"
                self.env_state = "Calculate"
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
                        ["", "cbrt", "^3", "nth_rt", "10^", "e^("],
                        ["", "FACT", "!", "asin", "acos", "atan"],
                        ["RECALL", "", "Abs", ",", "", "M-"]
                ]
                self.main_norm = [
                        ["7", "8", "9", "DEL", "AC"],  
                        ["4", "5", "6", "*", "÷"],  
                        ["1", "2", "3", "+", "-"],  
                        ["0", ".", "*10^", "Ans", "="]
                ]
                self.main_shift = [
                        ["CONST", "CONV", "RESET", "INS", "OFF"],
                        ["", "", "", "nPr", "nCr"],
                        ["", "", "", "Pol", "Rec"],
                        ["Rnd", "Ran#", pfe.pi_symbol, "%", ""]
                ]
                self.main_alpha = [
                        ["", "", "", "", ""],
                        ["", "", "", "gcd", "lcm"],
                        ["", "", "", "Int", ""],
                        ["", "RandInt", "e", "", ""]
                ]
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
                patch_entry_cursor(self.inputs)  

                self.output = tk.Entry(  
                        frame, font=("monospace", 16),  
                        justify="right", 
                )  
                self.output.pack(fill="x", pady=2)  

                def handle_enter(event):
                        self.equal_handle()
                        return "break"

                self.win.bind_all("<Return>", handle_enter)
                self.win.bind_all("<KP_Enter>", handle_enter)

        def _clear_entries(self):
                self.inputs.delete(0, tk.END)
                self.output.delete(0, tk.END)

        def _reset_finish_state(self, clear_output=True):
                self.finish_eval = False
                if clear_output:
                        self.output.delete(0, tk.END)

        def _restore_ans_input(self, text="Ans"):
                self.inputs.delete(0, tk.END)
                self.inputs.insert(0, text)
                self._reset_finish_state()

        def _rebuild_keypads(self):
                self.extra_frame.destroy()
                self.main_frame.destroy()
                self.build_extra_grid()
                self.build_main_grid()

        def _history_item(self, expr, result):
                if isinstance(result, (pfe.sqrt, float, pfe.Decimal, pfe.Fraction, pfe.Pi, pfe.euler_num)) or result < 1:
                        factors = []
                else:
                        factors = pfe.FACT(result)
                self.history.appendleft((expr, result, pfe.returning(result, "D"), factors))
                self.history_index = -1 # Đặt lại -1 khi có bài toán mới được tính toán
                self.current = expr

        def _show_result(self, expr, result):
                self.regulation = "S"
                self.fact_reg = "S"
                self.finish_eval = True
                self.output.delete(0, tk.END)
                self.output.insert(0, str(result))
                self._history_item(expr, result)

        def _show_tuple_result(self, result):
                self.finish_eval = True
                self.regulation = self.fact_reg = ""
                if result[-1] == "mod":
                        self.output.insert(0, f"{result[0]}, R={result[1]}")
                elif result[-1] == "pol":
                        self.output.insert(0, f"r={result[0]}, {pfe.theta_symbol}={result[1]}")
                elif result[-1] == "rec":
                        self.output.insert(0, f"x={result[0]}, y={result[1]}")

        def ensure_cursor_visible(self):
                """SỬA LỖI CUỘN MÀN HÌNH THEO CON TRỎ"""
                entry = self.inputs
                text = entry.get()
                if not text:
                        return

                pos = entry.index(tk.INSERT)
                entry.update_idletasks()
                
                # Đo kích thước vật lý của text để tính chính xác phần hiển thị
                left_ratio, right_ratio = entry.xview()
                n = len(text)
                current_ratio = pos / n

                # Nếu con trỏ lọt ra ngoài vùng nhìn thấy (bên trái hoặc bên phải)
                if current_ratio <= left_ratio:
                        entry.xview_moveto(max(0.0, (pos - 2) / n))
                elif current_ratio >= right_ratio:
                        entry.xview_moveto(min(1.0, (pos - int(n * (right_ratio - left_ratio)) + 3) / n))

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
                        self._clear_entries()
                        self.history.clear()
                        self.history_index = -1
                self._rebuild_keypads()

        def on_press2(self, value):
                """SỬA LỖI ĐIỀU HƯỚNG NÚT REPLAY (LEFT, RIGHT, UP, DOWN)"""
                self.inputs.focus_set()
                pos = self.inputs.index(tk.INSERT)
                text = self.inputs.get()
                
                if value == "<-":
                        limit = None
                        self.output.delete(0, tk.END)
                        if self.finish_eval:
                                self._reset_finish_state()
                                self.inputs.icursor(tk.END)
                        elif self.eval_state in ["solve_mode", "calc_finish"]:
                                self.eval_state = "eval"
                        elif self.eval_state == "calc_ready":
                                limit = 1
                        if limit is not None:
                                if pos - 1 <= limit: return
                        if pos > 0:
                                for token in sorted(SMART_TOKENS, key=len, reverse=True):
                                        L = len(token)
                                        if pos >= L and text[pos - L:pos] == token:
                                                self.inputs.icursor(pos - L)
                                                self.ensure_cursor_visible()
                                                return
                                self.inputs.icursor(pos-1)
                                self.ensure_cursor_visible()
                        elif pos == 0:
                                if not self.inputs.get() and not self.output.get():
                                        self.inputs.insert(0, self.current)
                                        self.inputs.icursor(tk.END)
                                        self.ensure_cursor_visible()
                                else: self.inputs.icursor(tk.END)
                                
                elif value == "->":
                        pos = self.inputs.index(tk.INSERT)
                        limit = None
                        self.output.delete(0, tk.END)
                        if self.finish_eval:
                                self._reset_finish_state()
                                self.inputs.icursor(0)
                        elif self.eval_state in ["solve_mode", "calc_finish"]:
                                self.eval_state = "eval"
                        elif self.eval_state == "calc_ready":
                                limit = 2
                        if pos < len(text):
                                for token in sorted(SMART_TOKENS, key=len, reverse=True):
                                        L = len(token)
                                        if text[pos:pos+L] == token:
                                                self.inputs.icursor(pos + L)
                                                self.ensure_cursor_visible()
                                                return
                                self.inputs.icursor(pos+1)
                                self.ensure_cursor_visible()
                        elif pos == len(text):
                                if not self.inputs.get() and not self.output.get():
                                        self.inputs.insert(0, self.current)
                                        self.inputs.icursor(tk.END)
                                        self.ensure_cursor_visible()
                                else: 
                                        if limit is not None:
                                                self.inputs.icursor(limit)
                                                self.ensure_cursor_visible()
                                        else:
                                                self.inputs.icursor(0)
                                                self.ensure_cursor_visible()
                                                
                elif value == "up":
                        # Lướt ngược dòng thời gian (về các phép toán cũ hơn)
                        if self.history:
                                if self.history_index < len(self.history) - 1:
                                        self.history_index += 1
                                contents = self.history[self.history_index]
                                self.inputs.delete(0, tk.END)
                                self.inputs.insert(0, contents[0])
                                self.inputs.icursor(tk.END)
                                self.output.delete(0, tk.END)
                                self.output.insert(0, str(contents[1]))
                                self.regulation = "S"
                                self.fact_reg = "S"
                                self.finish_eval = True
                                self.eval_state = "eval"
                                self.ensure_cursor_visible()
                        else:
                                self.inputs.icursor(0)
                                
                elif value == "down":
                        # Lướt xuôi dòng thời gian (về các phép toán mới hơn)
                        if self.history:
                                if self.history_index > 0:
                                        self.history_index -= 1
                                        contents = self.history[self.history_index]
                                        self.inputs.delete(0, tk.END)
                                        self.inputs.insert(0, contents[0])
                                        self.inputs.icursor(tk.END)
                                        self.output.delete(0, tk.END)
                                        self.output.insert(0, str(contents[1]))
                                else:
                                        # Nếu xuống hết cỡ thì xóa màn hình trống để nhập bài mới
                                        self.history_index = -1
                                        self._clear_entries()
                                        self.finish_eval = False
                                self.regulation = "S"
                                self.fact_reg = "S"
                                self.eval_state = "eval"
                                self.ensure_cursor_visible()
                        else:
                                self.inputs.icursor(tk.END)

        def on_press3(self, value):
                """Cho bảng số hàm (frac,...)"""
                self.inputs.focus_set()
                pos = self.inputs.index(tk.INSERT)
                if value == "^":
                        if self.finish_eval:
                                self._restore_ans_input()
                                pos = 3
                        expr = self.inputs.get()
                        if len(expr) > 0 and pos > 0:
                                if not expr[pos-1] in ["+", "-", "*", "/", "÷", "("]:
                                        text = value+"("
                                        self.inputs.insert(pos, value+"(")
                                        self.inputs.icursor(pos + len(text))
                        else:
                                text = value+"("
                                self.inputs.insert(pos, value+"(")
                                self.inputs.icursor(pos)
                        self.output.delete(0, tk.END)
                elif value in ["^2", "^3", "^-1"]:
                        expr = self.inputs.get()
                        if self.finish_eval:
                                self._restore_ans_input()
                                pos = 0
                        expr = self.inputs.get()
                        expo, num = value[0], value[1:]
                        text = expo + "(" + num + ")"
                        if len(expr) > 0 and pos > 0:
                                if not expr[pos-1] in ["+", "-", "*", "/", "÷", "("]:
                                        self.inputs.insert(pos, text)
                                        self.inputs.icursor(pos + len(text))
                        else:
                                self.inputs.insert(pos, text)
                                self.inputs.icursor(pos)
                        self.output.delete(0, tk.END)
                elif value in ([",", "_", "!", "="] + pfe.names):
                        if self.finish_eval:
                                self._reset_finish_state()
                        self.inputs.insert(pos, value)
                        self.inputs.icursor(pos + len(value))
                        self.output.delete(0, tk.END)
                elif value == "(":
                        if self.finish_eval:
                                self._reset_finish_state()
                        actual_text = "("
                        self.inputs.insert(pos, actual_text)
                        self.inputs.icursor(pos + 1)
                elif value == ")":
                        if self.finish_eval:
                                self._restore_ans_input(")")
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
                                elif 0 < pos < len(expr) and expr[pos-1] in ["+", "-", "*", "÷", "("]:
                                        self.inputs.insert(pos, "i")
                                        self.inputs.icursor(pos)
                                        self.output.delete(0, tk.END)
                                else:
                                        self.inputs.insert(pos, "i")
                                        self.inputs.icursor(pos+1)
                                        self.output.delete(0, tk.END)
                elif value in ["inte", "sqrt", "nth_rt", "log", "ln",
                               "sin", "cos", "tan", "asin", "acos", "atan",
                               "d_dx", "sums", "muls", "10^"]:
                        if self.finish_eval:
                                self._reset_finish_state()
                                self.inputs.delete(0, tk.END)
                                self.inputs.icursor(0)
                                pos = 0
                        expr = self.inputs.get()
                        text = ("*" if (0 < pos < len(expr) and \
                                        not any(expr[pos-len(i)] \
                                                for i in sorted(pfe.names + ["Ans", pfe.pi_symbol, "e"], 
                                                                key=len, 
                                                                reverse=True))) \
                                    else "") + value + "("
                        self.inputs.insert(pos, text)
                        self.inputs.icursor(pos + len(text))
                        self.output.delete(0, tk.END)
                elif value == "e^(":
                        if self.finish_eval:
                                self._reset_finish_state()
                                self.inputs.delete(0, tk.END)
                                self.inputs.icursor(0)
                                pos = 0
                        expr = self.inputs.get()
                        text = value
                        self.inputs.insert(pos, text)
                        self.inputs.icursor(pos + len(text))
                        self.output.delete(0, tk.END)
                elif value == "frac":
                        text = self.inputs.get()
                        pos = self.inputs.index(tk.INSERT)

                        # Reset sau khi vừa eval xong hoặc màn hình trống
                        if self.finish_eval or not text:
                                self._clear_entries()
                                self.inputs.insert(0, "()/()")
                                self.inputs.icursor(1)
                                return

                        # Tập hợp các token hợp lệ để nhận diện biến và hằng số từ pfe
                        VALID_TOKENS = sorted(
                                pfe.names + list(pfe.actual_val_const) + ["Ans", "e", "inf", pfe.pi_symbol],
                                key=len,
                                reverse=True
                        )

                        # --- CÁC HÀM HELPER PARSE CHUỖI NÂNG CẤP ---

                        def find_left_entity_bound(s, p):
                                if p <= 0: return 0
                                curr = p
                                while curr > 0:
                                        # 1. Nếu gặp dấu đóng ngoặc ')', có thể là hàm hoặc số mũ
                                        if s[curr-1] == ')':
                                                balance = 0
                                                idx = curr - 1
                                                found_open = False
                                                while idx >= 0:
                                                        if s[idx] == ')': balance += 1
                                                        elif s[idx] == '(': balance -= 1
                                                        if balance == 0:
                                                                idx_open = idx
                                                                found_open = True
                                                                break
                                                        idx -= 1
                                                
                                                if found_open:
                                                        # Nếu trước dấu '(' là '^', đây là khối số mũ ^(...) -> Quét tiếp sang trái tìm cơ số
                                                        if idx_open > 0 and s[idx_open-1] == '^':
                                                                curr = idx_open - 1
                                                                continue 
                                                        
                                                        # Nếu trước dấu '(' là tên hàm (sin, cos, sqrt...) -> Nuốt trọn hàm và quét tiếp
                                                        is_func = False
                                                        for token in sorted(SMART_TOKENS, key=len, reverse=True):
                                                                if token.endswith('('):
                                                                        L = len(token)
                                                                        if idx_open >= L - 1 and s[idx_open - L + 1 : idx_open + 1] == token:
                                                                                curr = idx_open - L + 1
                                                                                is_func = True
                                                                                break
                                                        if is_func:
                                                                continue
                                                        
                                                        # Nếu chỉ là ngoặc đơn thuần (...), vẫn thuộc chuỗi liên kết ẩn
                                                        curr = idx_open
                                                        continue
                                                else:
                                                        break
                                        
                                        # 2. Nếu là số thực hoặc chữ số
                                        if s[curr-1].isdigit() or s[curr-1] == '.':
                                                while curr > 0 and (s[curr-1].isdigit() or s[curr-1] == '.'):
                                                        curr -= 1
                                                continue
                                        
                                        # 3. Nếu là biến số hoặc hằng số toán học từ pfe
                                        found_token = False
                                        for token in VALID_TOKENS:
                                                L = len(token)
                                                if curr >= L and s[curr-L:curr] == token:
                                                        curr -= L
                                                        found_token = True
                                                        break
                                        if found_token:
                                                continue
                                                
                                        # Gặp toán tử (+ - * ÷) công khai -> Đứt chuỗi nhân ẩn, dừng lại tại đây
                                        break
                                return curr

                        def find_right_entity_bound(s, p):
                                if p >= len(s): return len(s)
                                curr = p
                                
                                # 1. Kiểm tra xem có bắt đầu bằng một hàm số không (sin, cos...)
                                found_func = False
                                for token in sorted(SMART_TOKENS, key=len, reverse=True):
                                        if token.endswith('('):
                                                L = len(token)
                                                if s[curr:curr+L] == token:
                                                        curr += L
                                                        balance = 1
                                                        while curr < len(s):
                                                                if s[curr] == '(': balance += 1
                                                                elif s[curr] == ')': balance -= 1
                                                                curr += 1
                                                                if balance == 0: break
                                                        found_func = True
                                                        break
                                
                                if not found_func:
                                        # 2. Kiểm tra nếu là một số
                                        if s[curr].isdigit() or s[curr] == '.':
                                                while curr < len(s) and (s[curr].isdigit() or s[curr] == '.'):
                                                        curr += 1
                                        else:
                                                # 3. Kiểm tra nếu là một biến/hằng số từ pfe
                                                found_token = False
                                                for token in VALID_TOKENS:
                                                        L = len(token)
                                                        if s[curr:curr+L] == token:
                                                                curr += L
                                                                found_token = True
                                                                break
                                
                                # HẬU XỬ LÝ: Nếu ngay sau thực thể bên phải này dính liền với số mũ ^(...), ta phải nuốt luôn số mũ đó
                                if curr < len(s) and s[curr:curr+2] == '^(':
                                        curr += 2
                                        balance = 1
                                        while curr < len(s):
                                                if s[curr] == '(': balance += 1
                                                elif s[curr] == ')': balance -= 1
                                                curr += 1
                                                if balance == 0: break
                                                
                                return curr

                        # --- ĐIỀU HƯỚNG VÀ CHÈN PHÂN SỐ CHUẨN XÁC ---
                        left_part = text[:pos]
                        right_part = text[pos:]

                        # Nếu ngay trước con trỏ là toán tử rõ ràng hoặc mở ngoặc (ví dụ: 2+| hoặc 3^(| )
                        if left_part and (left_part[-1] in ["+", "-", "*", "÷"] or left_part.endswith("^(") or left_part[-1] == "("):
                                self.inputs.insert(pos, "()/()")
                                self.inputs.icursor(pos + 1)
                                return

                        # Tiến hành quét tìm biên giới hạn thực thể
                        left_bound = find_left_entity_bound(text, pos)
                        right_bound = find_right_entity_bound(text, pos)

                        left_entity = text[left_bound:pos]
                        right_entity = text[pos:right_bound]

                        inside_func = (left_part.count('(') > left_part.count(')'))

                        if inside_func:
                                if left_entity and right_entity:
                                        new_text = text[:left_bound] + f"({left_entity})/({right_entity})" + text[right_bound:]
                                        cursor_pos = left_bound + len(f"({left_entity})/({right_entity})")
                                elif left_entity and not right_entity:
                                        new_text = text[:left_bound] + f"({left_entity})/()" + text[pos:]
                                        cursor_pos = left_bound + len(f"({left_entity})/") + 1
                                else:
                                        new_text = text[:pos] + f"()/{right_entity}" + text[right_bound:]
                                        cursor_pos = pos + 1
                        else:
                                # Ở ngoài hàm (Ngoại vi - Đáp ứng trực tiếp Trường hợp 1, 2, 3 mới)
                                if left_entity and right_entity:
                                        new_text = text[:left_bound] + f"({left_entity})/({right_entity})" + text[right_bound:]
                                        # Đưa con trỏ ra phía sau phân số vừa tạo như Casio thật
                                        cursor_pos = left_bound + len(f"({left_entity})/({right_entity})")
                                        
                                elif left_entity and not right_entity:
                                        new_text = text[:left_bound] + f"({left_entity})/()" + text[pos:]
                                        cursor_pos = left_bound + len(f"({left_entity})/") + 1
                                        
                                elif not left_entity and right_entity:
                                        new_text = text[:pos] + f"()/{right_entity}" + text[right_bound:]
                                        cursor_pos = pos + 1
                                else:
                                        new_text = text[:pos] + "()/" + text[pos:]
                                        cursor_pos = pos + 1

                        self.inputs.delete(0, tk.END)
                        self.inputs.insert(0, new_text)
                        self.inputs.icursor(cursor_pos)

                        self.output.delete(0, tk.END)
                        self.ensure_cursor_visible()
                elif value == "cbrt":
                        if self.finish_eval:
                                self._reset_finish_state()
                                self.inputs.delete(0, tk.END)
                                self.inputs.icursor(0)
                                pos = 0
                        expr = self.inputs.get()
                        text = ("*" if (pos > 0 and \
                                        not any(expr[pos-len(i)] \
                                                for i in sorted(pfe.names + ["Ans", pfe.pi_symbol, "e"], 
                                                                key=len, 
                                                                reverse=True))) \
                                    else "") + "nth_rt(3,"
                        self.inputs.insert(pos, text)
                        self.inputs.icursor(pos + len(text))
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
                                        self.eval_state = "solve_mode_calc"
                                        self.solve_expr = expr
                                        self.solve_vars = free_symbol
                                        self.solve_values = {}
                                        self.solve_index = 0
                                        self.inputs.delete(0, tk.END)
                                        self.output.delete(0, tk.END)
                                        self.inputs.insert(0, f"{free_symbol[0]}=")
                                else:
                                        self.eval_state = "solve_mode"
                                        self.output.delete(0, tk.END)
                                        self.current = expr
                                        sol = pfe.solve_eq(expr)
                                        if isinstance(sol, list) and len(sol) == 0:
                                                self.output.insert(0, "No solution.")
                                        else:
                                                self.output.insert(0, f"x={sol}")
                        except Exception as ex:
                                self.output.delete(0, tk.END)
                                self.output.insert(0, ex)
                elif value == "CALC":
                        if self.finish_eval:
                                self._reset_finish_state()
                        expr = self.inputs.get()
                        free_symbol = []
                        for i in pfe.names:
                                if i in expr:
                                        free_symbol.append(i)
                        try:
                                if free_symbol:
                                        self.eval_state = "calc_ready"
                                        self.calc_expr = expr
                                        self.calc_vars = free_symbol
                                        self.calc_values = {}
                                        self.calc_index = 0
                                        self.inputs.delete(0, tk.END)
                                        self.output.delete(0, tk.END)
                                        self.inputs.insert(0, f"{free_symbol[0]}=")
                                else:
                                        expr = self.inputs.get()
                                        if "=" in expr:
                                                self.output.insert(0, MATH_ERROR)
                                                self.fact_reg = self.regulation = ""
                                                self.finish_eval = True
                                                return
                                        result = pfe.evaluate_expression(expr)
                                        if isinstance(result, tuple):
                                                self._show_tuple_result(result)
                                        else:
                                                self._show_result(expr, result)
                        except Exception as ex:
                                self.regulation = self.fact_reg = ""
                                self.output.delete(0, tk.END)
                                self.output.insert(0, ex)
                                self.finish_eval = True
                                self.current = expr
                elif value == "Abs":
                        if self.finish_eval:
                                self._reset_finish_state()
                        self.inputs.insert(pos, "||")
                        self.inputs.icursor(pos+1)
                elif value == "[mod]":
                        if self.finish_eval:
                                self._reset_finish_state()
                        self.inputs.insert(pos, "[mod]")
                        self.inputs.icursor(pos+len("[mod]"))
                elif value == "OPTN":
                        pass
                elif value == "S<=>D" and self.history and self.finish_eval:
                        self.output.delete(0, tk.END)
                        idx = self.history_index if self.history_index != -1 else 0
                        if self.regulation == "S":
                                self.output.insert(0, self.history[idx][2])
                                self.regulation = "D"
                        else:
                                self.output.insert(0, self.history[idx][1])
                                self.regulation = "S"
                elif value == "FACT" and self.history and self.finish_eval:
                        idx = self.history_index if self.history_index != -1 else 0
                        if self.fact_reg == "S":
                                if isinstance(self.history[idx][1], complex):
                                        pass
                                elif self.history[idx][3]:
                                        factors = self.history[idx][3]
                                        text = "*".join(map(lambda x: "^(".join(map(str, x)) + ")", factors))
                                        self.output.insert(0, text)
                                        self.fact_reg = "N"
                        elif self.fact_reg == "N":
                                self.output.delete(0, tk.END)
                                self.output.insert(0, str(self.history[idx][2]))
                                self.fact_reg = "S"

                if self.shift or self.alpha:
                        self.shift = self.alpha = False
                        self._rebuild_keypads()
                self.ensure_cursor_visible()

        def equal_handle(self):
                self.output.delete(0, tk.END)
                expr = self.inputs.get()
                if self.eval_state == "eval":
                        try:
                                expr = self.inputs.get()
                                if "=" in expr:
                                        self.output.insert(0, MATH_ERROR)
                                        self.fact_reg = self.regulation = ""
                                        self.finish_eval = True
                                        return
                                with open("new_run.txt", "a") as f:
                                        print(f'{expr} -> {pfe.preprocess_expression(expr)}\n', end='', file=f)
                                result = pfe.evaluate_expression(expr)
                                if isinstance(result, tuple):
                                        self._show_tuple_result(result)
                                else:
                                        self._show_result(expr, result)
                        except Exception as ex:
                                self.regulation = self.fact_reg = ""
                                self.output.delete(0, tk.END)
                                self.output.insert(0, ex)
                                self.finish_eval = True
                                self.current = expr
                elif self.eval_state == "solve_mode_calc":
                        if self.solve_index < len(self.solve_vars):
                                var, val = self.inputs.get().split("=")
                                if val != "": 
                                        self.solve_values[var] = pfe.evaluate_expression(val)
                                self.solve_index += 1
                                self.inputs.delete(0, tk.END)
                                self.inputs.insert(0, f"{self.solve_vars[self.solve_index]}=")
                        else:
                                self.inputs.delete(0, tk.END)
                                result = pfe.solve_eq(self.solve_expr, **self.solve_values)
                                self.inputs.insert(0, self.solve_expr)
                                self.output.insert(0, str(result))
                                self.current = self.solve_expr
                                self.eval_state = "solve_mode"
                elif self.eval_state == "calc_ready":
                        try:
                                if self.calc_index < len(self.calc_vars):
                                        calcs = self.inputs.get()
                                        if calcs[1:] != "=": 
                                                var, val = self.inputs.get().split("=")
                                                self.calc_values[var] = pfe.evaluate_expression(val)
                                        self.calc_index += 1
                                        if not self.calc_index < len(self.calc_vars): 
                                                self.inputs.delete(0, tk.END)
                                                self.inputs.insert(0, self.calc_expr)
                                                result = pfe.calc(self.calc_expr, **self.calc_values)
                                                if isinstance(result, tuple):
                                                                self._show_tuple_result(result)
                                                else:
                                                                self._show_result(self.calc_expr, result)
                                                self.eval_state = "calc_finish" 
                                                return
                                        self.inputs.delete(0, tk.END)
                                        self.inputs.insert(0, f"{self.calc_vars[self.calc_index]}=")
                                else:
                                        self.inputs.delete(0, tk.END)
                                        self.inputs.insert(0, self.calc_expr)
                                        result = pfe.calc(self.calc_expr, **self.calc_values)
                                        if isinstance(result, tuple):
                                                self.finish_eval = True
                                                self.regulation = self.fact_reg = ""
                                                if result[-1] == "mod":
                                                        self.output.insert(0, f"{result[0]}, R={result[1]}")
                                                elif result[-1] == "pol":
                                                        self.output.insert(0, f"r={result[0]}, {pfe.theta_symbol}={result[1]}")
                                                elif result[-1] == "rec":
                                                        self.output.insert(0, f"x={result[0]}, y={result[1]}")
                                        else:
                                                self._show_result(self.calc_expr, result)
                                        self.eval_state = "calc_finish"
                        except Exception as ex:
                                self.eval_state = "eval"
                                self.regulation = self.fact_reg = ""
                                self.output.delete(0, tk.END)
                                self.output.insert(0, ex)
                                self.finish_eval = True
                                self.current = self.calc_expr
                elif self.eval_state == "calc_finish":
                        if self.finish_eval:
                                self.finish_eval = False
                        self.eval_state = "calc_ready"
                        self.calc_index = 0
                        self.inputs.delete(0, tk.END)
                        self.output.delete(0, tk.END)
                        self.inputs.insert(0, f"{self.calc_vars[0]}=")

        def on_press4(self, value):
                self.inputs.focus_set()
                pos = self.inputs.index(tk.INSERT)
                if value == "AC":
                        self._reset_finish_state()
                        self.eval_state = "eval"
                        self._clear_entries()
                        self.history_index = -1
                elif value == "DEL":
                        self.finish_eval = False
                        text = self.inputs.get()
                        del_right = False
                        if pos == 0:
                                del_right = True
                        for token in sorted(SMART_TOKENS, key=len, reverse=True):
                                L = len(token)
                                if pos >= L and text[pos - L:pos] == token:
                                        self.inputs.delete(pos - L, pos)
                                        self.inputs.icursor(pos - L)
                                        self.ensure_cursor_visible()
                                        return
                                elif del_right and text[pos:pos + L] == token:
                                        self.inputs.delete(pos, pos + L)
                                        self.inputs.icursor(pos)
                                        self.ensure_cursor_visible()
                                        return
                        if del_right:
                                self.inputs.delete(pos, pos+1)
                                self.inputs.icursor(pos)
                        else:
                                self.inputs.delete(pos - 1, pos)
                                self.inputs.icursor(pos - 1)
                        self.output.delete(0, tk.END)
                elif value == "=":
                        self.equal_handle()
                elif value == "OFF":
                        exit(0)
                elif value in ["Int", "Pol", "Rnd", "RandInt", "Rec"]:
                        if self.finish_eval:
                                self._clear_entries()
                                self.finish_eval = False
                        text = value + "("
                        self.inputs.insert(pos, text)
                        self.inputs.icursor(pos+len(text)-1)
                elif value in "+-*÷/":
                        if self.finish_eval:
                                self._clear_entries()
                                self.finish_eval = False
                                self.inputs.insert(0, "Ans" + value)
                                self.inputs.icursor(tk.END)
                                return
                        self.inputs.insert(pos, value)
                        self.inputs.icursor(pos+1)
                elif value in [str(i) for i in range(10)]:
                        if self.finish_eval:
                                self._clear_entries()
                                self.finish_eval = False
                                self.inputs.insert(0, value)
                                self.inputs.icursor(tk.END)
                                return
                        self.inputs.insert(pos, value)
                        self.inputs.icursor(pos+1)
                elif value == "nCr":
                        if self.finish_eval:
                                self._clear_entries()
                                self.finish_eval = False
                                self.inputs.insert(0, "Ans_C_")
                                self.inputs.icursor(len("Ans_C_"))
                        else:
                                self.inputs.insert(pos, "_C_")
                                self.inputs.icursor(pos+3)
                elif value == "nPr":
                        if self.finish_eval:
                                self._clear_entries()
                                self.finish_eval = False
                                self.inputs.insert(0, "Ans_P_")
                                self.inputs.icursor(len("Ans_P_"))
                        else:
                                self.inputs.insert(pos, "_P_")
                                self.inputs.icursor(pos+3)
                elif value == "*10^":
                        if self.finish_eval:
                                self._clear_entries()
                                self.finish_eval = False
                                pos = 0
                        self.inputs.insert(pos, value+"(")
                        expr = self.inputs.get()
                        if pos == 0:
                                self.inputs.icursor(pos)
                        else: 
                                if len(expr) > 0:
                                        if not expr[pos-1] in "+-*/÷(":
                                                self.inputs.icursor(pos+len(value+"("))
                                        else: self.inputs.icursor(pos)
                elif value == "CONST":
                        pass
                elif value == "CONV":
                        pass
                elif value == "INS":
                        pass
                else:
                        self.output.delete(0, tk.END)
                        pos = self.inputs.index(tk.INSERT)
                        if self.finish_eval:
                                self.inputs.delete(0, tk.END)
                                pos = 0
                                self._reset_finish_state(clear_output=False)
                        self.inputs.insert(pos, value)
                        self.inputs.icursor(pos + len(value))
                        
                if self.shift or self.alpha:
                        self.shift = self.alpha = False
                        self._rebuild_keypads()
                self.ensure_cursor_visible()

        def build_top_keys(self):  
                frame = tk.Frame(self.win)  
                frame.pack(pady=4)  
                for i, txt in enumerate(["SHIFT", "ALPHA", "MODE", "ON"]):
                        btn = tk.Button(frame, text=txt, width=4, height=1, takefocus=0)
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
                        btn = tk.Button(frame, text=a, width=2, height=1, takefocus=0, state="disabled" if a == "" else "normal")
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
                if self.shift:
                        grid = self.extra_shift
                        self.extra_color = TEXT_ACTIVE
                elif self.alpha:
                        grid = self.extra_alpha
                        self.extra_color = TEXT_ALPHA
                else:
                        grid = self.extra_norm
                        self.extra_color = TEXT_NORMAL

                for r in range(len(grid)):  
                        for c in range(len(grid[0])):
                                txt = grid[r][c]
                                btn = tk.Button(self.extra_frame, text=txt, width=2, height=2, state="disabled" if txt == "" else "normal", takefocus=0)
                                btn.grid(row=r, column=c, padx=2, pady=2)
                                btn.bind("<Button-1>", lambda e, t=txt: self.on_press3(t))
                                btn.config(fg=self.extra_color, bg="#00cbff")

        def build_main_grid(self):  
                self.main_frame = tk.Frame(self.win)
                self.main_frame.pack(pady=6)
                if self.shift:
                        grid = self.main_shift
                        self.main_color = TEXT_ACTIVE
                elif self.alpha:
                        grid = self.main_alpha
                        self.main_color = TEXT_ALPHA
                else:
                        grid = self.main_norm
                        self.main_color = TEXT_NORMAL
                for r, row in enumerate(grid):  
                        for c, txt in enumerate(row):  
                                btn = tk.Button(self.main_frame, text=txt, width=4, height=3, takefocus=0)
                                btn.grid(row=r, column=c, padx=2, pady=2)
                                btn.bind("<Button-1>", lambda e, t=txt: self.on_press4(t))
                                btn.config(fg=self.main_color, bg="#00cbff")
                                
        def run(self):  
                self.win.mainloop()  

Calculator_fx().run()
