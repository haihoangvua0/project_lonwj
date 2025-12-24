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

def phuong_sai_hieu_chinh(l: list[int | Fraction | float | Decimal],
                          freq: list[int | Fraction | float | Decimal] | None = None):
        n = len(l)
        return returning(((n - 1) / n) * phuong_sai(l, freq))
