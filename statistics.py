"""Statistics functions (Repaired and Collected; updating is in progress)"""
from process_front_end import *
from collections import Counter

stat_setting(1)
choice = dict_of_setting["Statistics"]

def customised_sorted(vals: list[int | Fraction | float | Decimal],
                      freq: list[int | Fraction | float | Decimal]):
        new = list(zip(vals, freq))
        new.sort(key=lambda x: x[0])
        vals = [x1 for x1,_ in new]
        freq = [x2 for _,x2 in new]
        return vals, freq

def pre_sum(l: list[int | Fraction | float | Decimal]
) -> list[int | Fraction | float | Decimal]:
        a = [0 for _ in l]
        for i in range(len(l)):
                if i == 0:
                        a[0] = l[0]
                        continue
                a[i] = a[i - 1] + l[i]
        return a

def value_at_k(vals: list[int | Fraction | float | Decimal], 
               freq: list[int | Fraction | float | Decimal], 
               k: int
):
        pre_sum_freq = pre_sum(freq)
        for i in range(len(pre_sum_freq)):
                if k > pre_sum_freq[i]:
                        continue
                else:
                        break
        return vals[i]

def median_freq(vals: list[int | Fraction | float | Decimal],
                freq: list[int | Fraction | float | Decimal]
) -> int | Fraction | float | Decimal:
        vals, freq = customised_sorted(vals, freq)
        n = sum(freq)
        if n % 2 == 0:
                k1 = n // 2
                k2 = k1 + 1
                val1 = value_at_k(vals, freq, k1)
                val2 = value_at_k(vals, freq, k2)
                return returning((1/2) * (val1 + val2))
        else:
                k = (n - 1) // 2 + 1
                value_ = value_at_k(vals, freq, k)
                return returning(value_)
                
def quartiles_freq(vals: list[int | Fraction | float | Decimal],
                   freq: list[int | Fraction | float | Decimal]
) -> tuple[int | Fraction | float | Decimal]:
        vals, freq = customised_sorted(vals, freq)
        Q2 = median_freq(vals, freq)
        n = sum(freq)
        if n % 2 == 0:
                n1 = n // 2
                if n1 % 2 == 0:
                        k1 = n1 // 2
                        k2 = k1 + 1
                        val1 = value_at_k(vals, freq, k1)
                        val2 = value_at_k(vals, freq, k2)
                        Q1 = returning((1/2) * (val1 + val2))
                        k3 = k1 + n1
                        k4 = k3 + 1
                        val3 = value_at_k(vals, freq, k3)
                        val4 = value_at_k(vals, freq, k4)
                        Q3 = returning((1/2) * (val3 + val4))
                        return Q1, Q2, Q3
                else:
                        k1 = ((n1 - 1) // 2) + 1
                        k3 = k1 + n1
                        val1 = value_at_k(vals, freq, k1)
                        val3 = value_at_k(vals, freq, k3)
                        Q1 = val1
                        Q3 = val3
                        return Q1, Q2, Q3
        else:
                n2 = (n - 1) // 2
                if n2 % 2 == 0:
                        k1 = n2 // 2
                        k2 = k1 + 1
                        val1 = value_at_k(vals, freq, k1)
                        val2 = value_at_k(vals, freq, k2)
                        Q1 = returning((1/2) * (val1 + val2))
                        k3 = k1 + n2 + 1
                        k4 = k3 + 1
                        val3 = value_at_k(vals, freq, k3)
                        val4 = value_at_k(vals, freq, k4)
                        Q3 = returning((1/2) * (val3 + val4))
                        return Q1, Q2, Q3
                else:
                        k1 = ((n2 - 1) // 2) + 1
                        k3 = k1 + n2 + 1
                        val1 = value_at_k(vals, freq, k1)
                        val3 = value_at_k(vals, freq, k3)
                        Q1 = val1
                        Q3 = val3
                        return Q1, Q2, Q3

def median(l: list, freq: list | None = None):
        global choice
        if freq:
                n = len(l)
                if choice == 0:
                        #print("Running here 1")
                        #freq = None
                        l = sorted(l)
                        n = len(l)
                        if n % 2 == 0:
                                k = n // 2
                                res = (1/2) * (l[k - 1] + l[k])
                                res = returning(res)
                                return res
                        else:
                                k = (n - 1) // 2
                                return returning(l[k])
                return median_freq(l, freq)
        else:
                freq = [1 for _ in l]
                return median(l, freq)

def tu_phan_vi(l: list, freq: list | None = None):
        global choice
        if freq and freq is not None:
                if not choice:
                        l = sorted(l)
                        n = len(l)
                        print(l)
                        q2 = median(l)
                        if n % 2 == 0: 
                                new = l[:(n // 2)]
                                new1 = l[(n // 2) + 1:]
                                q1 = median(new)
                                q3 = median(new1)
                                return (q1, q2, q3)
                        else:
                                k = (n - 1) // 2
                                new = l[:k]
                                new1 = l[k + 1:]
                                q1 = median(new)
                                q3 = median(new1)
                                return (q1, q2, q3)
                return quartiles_freq(l, freq)
        else:   
                freq = [1 for _ in l]
                return tu_phan_vi(l, freq)

def hi(l: list, freq: list | None = None):
        if not freq or freq is None:
                new = Counter(l)
                return new.most_common(1)[0][0]
        idx = freq.index(max(freq))
        return l[idx]

def mean(l: list, freq: list | None = None):
        global choice
        if freq is not None and freq:
                if not choice:
                        res = sum(l) / len(l)
                        #res = int(res) if res.is_integer() else res
                        return returning(res)
                miss = len(l) - len(freq)
                n = sum(freq)
                if miss:
                        fill = [1 for _ in range(miss)]
                        freq += fill
                res = sum(l[i] * freq[i] for i in range(len(l))) / n
                return returning(res)
        else:
                freq = [1 for _ in l]
                return mean(l, freq)

def phuong_sai(l: list, freq: list | None = None):
        if freq is None or not freq:
                n = len(l)
                mean_ = sum(l) / n
                return sum((x - mean_)**2 for x in l) / n
        else:
                n = sum(freq)
                mean_ = mean(l, freq)
                return sum(freq[i] * (l[i] - mean_)**2 for i in range(len(l))) / n
        
def do_lech_chuan(l: list, freq: list | None = None):
        return pow(phuong_sai(l, freq), 0.5)

def phuong_sai_hieu_chinh(l: list[int | Fraction | float | Decimal],
                          freq: list[int | Fraction | float | Decimal] | None = None):
        if freq is None or not freq:
                n = len(l)
        else:
                n = sum(freq)

        return returning((n / (n - 1)) * phuong_sai(l, freq))

def khoang_bien_thien(l: list, freq: list | None = None):
        return returning(max(l) - min(l))

def khoang_tu_phan_vi(l: list, freq: list | None = None):
        if not freq or freq is None:
                freq = [1 for _ in l]
    
        Q1, _, Q3 = tu_phan_vi(l, freq)
        return returning(Q3 - Q1)

def Sum_x2(l: list[int | Fraction | float | Decimal],
           freq: list[int | Fraction | float | Decimal] | None = None):
        if freq and freq is not None:
                s = 0
                if choice:
                        for i in range(len(l)):
                                s += freq[i] * l[i]**2
                        return returning(s)
                s = 0
                for i in l:
                        s += i ** 2
                return returning(s)
        else:
                freq = [1 for _ in range(l)]
                return Sum_x2(l, freq)

def Sum_x(l: list[int | Fraction | float | Decimal],
          freq: list[int | Fraction | float | Decimal] | None = None):
        if freq and freq is not None:
                if choice:
                        s = 0
                        for i in range(len(l)):
                                s += l[i] * freq[i]
                        return returning(s)
                return sum(l)
        else:
                freq = [1 for _ in l]
                return Sum_x(l, freq)
if __name__ == "__main__":
        print("=== THỐNG KÊ DỮ LIỆU (SGK LỚP 10) ===")
    
        # Nhập dữ liệu
        raw_vals = input("Nhập các giá trị (cách nhau bằng khoảng trắng): ").strip()
        raw_freq = input("Nhập tần số tương ứng (để trống nếu không có): ").strip()
    
        l = list(map(evaluate_expression, raw_vals.split()))
    
        if raw_freq:
                freq = list(map(lambda x: evaluate_expression(x), raw_freq.split()))
                if len(freq) != len(l):
                        exit("Số lượng giá trị và tần số không khớp!")
        else:
                freq = None

        print("\n--- CÁC ĐẠI LƯỢNG THỐNG KÊ ---")
        
        # Số lượng
        n = sum(freq) if freq else len(l)
        print(f"{n = }")
        # Trung bình
        print("Trung bình:", mean(l, freq))

        # Trung vị
        print("Trung vị:", median(l, freq))

        # Tứ phân vị
        q1, q2, q3 = tu_phan_vi(l, freq)
        print("Q1 =", q1)
        print("Q2 =", q2)
        print("Q3 =", q3)

        # Mốt
        print("Mốt:", hi(l, freq))

        # Khoảng biến thiên
        print("Khoảng biến thiên:", khoang_bien_thien(l, freq))

        # Khoảng tứ phân vị
        print("Khoảng tứ phân vị:", khoang_tu_phan_vi(l, freq))

        # Phương sai & độ lệch chuẩn
        print("Phương sai:", phuong_sai(l, freq))
        print("Độ lệch chuẩn:", do_lech_chuan(l, freq))
        print("Phương sai hiệu chỉnh:", phuong_sai_hieu_chinh(l, freq))

        # Tổng
        print("Tổng x:", Sum_x(l, freq))
        print("Tổng x^2:", Sum_x2(l, freq))
        print("\n=== KẾT THÚC ===")
