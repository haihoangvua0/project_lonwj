from process_front_end import *

choice = dict_of_setting["Statistics"]
def fast(l: list[int]):
        fast = []
        for i in range(len(l)):
                if i == 0:
                        fast.append(l[0])
                        continue
                fast.append(fast[i-1] + l[i])
        return fast

def median(l: list[int], freq: list | None = None):
        global choice
        if freq:
                if not choice:
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
                        
                import bisect
                presum_freq = fast(freq)
                pass

        else:
                if choice:
                        freq = [1 for _ in l]
                        presum_freq = fast(freq)
                        pass
                
                


# min, max

def tu_phan_vi(l: list[int]):
        l = sorted(l)
        n = len(l)
        print(l)
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
        a = [5.73, 7.05, 6.77, 1.82, 5.64, 6.42]
        print(tu_phan_vi(a))
