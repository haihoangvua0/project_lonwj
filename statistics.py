"""Statistics functions (Repaired and Collected; updating is in progress)"""
from process_front_end import *
from collections import Counter

stat_setting(1)
choice = dict_of_setting["Statistics"]

def value_at_k(values: list, freq: list, *, k: int = 0):
        """
        Trả về giá trị ứng với phần tử thứ k
        (đếm từ trái sang phải, đúng kiểu SGK)
        """
        count = 0
        for i in range(len(values)):
                count += freq[i]
                if count >= k:
                        return values[i]
def median_freq(values: list, freq: list):
        # Sắp xếp theo giá trị
        data = sorted(zip(values, freq), key=lambda x: x[0])
        values = [x for x, _ in data]
        freq   = [f for _, f in data]
    
        N = sum(freq)
    
        if N % 2 == 1:
                k = (N + 1) // 2
                return returning(value_at_k(values, freq, k=k))
        else:
                k1 = N // 2
                k2 = k1 + 1
                x1 = value_at_k(values, freq, k = k1)
                x2 = value_at_k(values, freq, k = k2)
                return returning((x1 + x2) / 2)
def quartiles_freq(values: list, freq: list):
        data = sorted(zip(values, freq), key=lambda x: x[0])
        values = [x for x, _ in data]
        freq   = [f for _, f in data]
    
        N = sum(freq)
        def get_quartile(pos: int | float | Fraction):
                if pos.is_integer():
                        return value_at_k(values, freq, k=int(pos))
                else:
                        k1 = int(pos)
                        k2 = k1 + 1
                        x1 = value_at_k(values, freq, k=k1)
                        x2 = value_at_k(values, freq, k=k2)
                        return returning((x1 + x2) / 2)
    
        Q1 = get_quartile((N + 1) / 4)
        Q2 = get_quartile((N + 1) / 2)
        Q3 = get_quartile(3 * (N + 1) / 4)
    
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
                                new = l[:(n // 2) + 1]
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
        length = len(l)
        if not freq:
                if choice:
                        freq = [1 for _ in l]
                        return phuong_sai(l, freq)
                #length = len(l)
                mean_ = sum(l) / length
                s: float = 0
                for i in l:
                        s += ((i - mean_)**2) / length
                #s = int(s) if s.is_integer() else s
                return s
        else:
                n = sum(freq)
                x_ = mean(l)
                s = 0
                for i in range(length):
                        s += (freq[i] * (l[i] - x_)**2) / n
                s = returning(s)
                return s
def do_lech_chuan(l: list, freq: list | None = None):
        return pow(phuong_sai(l, freq), 0.5)

def khoang_bien_thien(l: list, freq: list | None = None):
        if not freq or freq is None:
                l = sorted(l)
                return returning(l[-1] - l[0])
        # Có tần số
        data = sorted(zip(l, freq), key=lambda x: x[0])
        values = [x for x, _ in data]
        return returning(values[-1] - values[0])

def khoang_tu_phan_vi(l: list, freq: list | None = None):
        if not freq or freq is None:
                freq = [1 for _ in l]
    
        Q1, _, Q3 = tu_phan_vi(l, freq)
        return returning(Q3 - Q1)

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

    #print("\n--- DỮ LIỆU SAU XỬ LÍ ---")
#    if freq:
#        for v, f in zip(l, freq):
#            print(f"Giá trị {v} xuất hiện {f} lần")
#    else:
#        print(l)

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

        print("\n=== KẾT THÚC ===")
