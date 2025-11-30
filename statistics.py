from process_front_end import *
def median(l: list[int]):
        l = sorted(l)
        n = len(l)
        if n % 2 == 0:
                k = n // 2
                res = (1/2) * (l[k - 1] + l[k])
                res = int(res) if res.is_integer() else res
                return res
        else:
                k = (n - 1) // 2
                return (l[k])

# min, max

def tu_phan_vi(l: list[int]):
        l = sorted(l)
        n = len(l)
        q2 = median(l)
        if n % 2 == 0: 
                new = l[:(n // 2) + 1] + [q2]
                new1 = [q2] + l[(n // 2) + 1:]
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


def hi(l: list[int]):
        from collections import Counter
        new = Counter(l)
        return list(new.most_common(1)[0])[0]

def mean(l: list[int]):
        res = sum(l) / len(l)
        res = int(res) if res.is_integer() else res
        return res

def phuong_sai(l: list[int], freq: list[int] = []):
        length = len(l)
        if not freq:
                #length = len(l)
                mean_ = sum(l) / length
                s: float = 0
                for i in l:
                        s += ((i - mean_)**2) / length
                s = int(s) if s.is_integer() else s
                return s
        else:
                n = sum(freq)
                x_ = mean(l)
                s = 0
                for i in range(length):
                        s += (freq[i] * (l[i] - x_)**2) / n
                s = int(s) if s.is_integer() else s
                return s
def do_lech_chuan(l: list[int], freq: list[int] = []):
        return pow(phuong_sai(l, freq), 0.5)

if __name__ == "__main__":
        print()
