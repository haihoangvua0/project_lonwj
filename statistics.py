"""Correcting... Cannot actually use at the moment"""
from process_front_end import *
from collections import Counter

stat_setting(1)
choice = dict_of_setting["Statistics"]
#def fast(l: list[int]):
#        fast = []
#        for i in range(len(l)):
#                if i == 0:
#                        fast.append(l[0])
#                        continue
#                fast.append(fast[i-1] + l[i])
#        return fast

def median(l: list[int], freq: list | None = None, *, need: bool = False):
        # Control the reputation in list of vals
        global choice
        #choice = 1
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
                # Check the length of the list 'frequency'
                #print("Running here 2")
                import bisect
                alls = [(k, f) for k, f in zip(l, freq)]
                alls.sort(key=lambda x: x[0])
                freq = [i[1] for i in alls]
                l = [i[0] for i in alls]
                #presum_freq = fast(freq)
                pre_s = sum(freq)
                if pre_s % 2 == 0:
                        k = (pre_s // 2)
                        k_ = k + 1
                        pos1 = 0; pos2 = 0
                        for i in freq:
                                k -= i
                                if k > 0:
                                        pos1 += 1
                                else: 
                                        k = abs(k)
                                        break
                        
                        for i_ in freq:
                                k_ -= i_
                                if k_ > 0:
                                        pos2 += 1
                                else: 
                                        k_ = abs(k_)
                        res = returning((1/2) * (l[pos1] + l[pos2]))
                        if need:
                                return (res, pos1, pos2, k, k_)
                        #print(l[pos1], l[pos2])
                        return res
                else:
                        #print("Running here 3")
                        k = (pre_s - 1) // 2 + 1
                        pos = 0
                        for i in freq:
                                k -= i
                                if k > 0:
                                        pos += 1
                                else: 
                                        k = abs(k)
                                        break
                        res = returning(l[pos])
                        if need:
                                return (res, pos, k)
                        return res
        else:
                freq = [1 for _ in l]
                return median(l, freq)
# min, max

def tu_phan_vi(l: list, freq: list | None = None):
        global choice
        if freq and freq is not None:
                if not choice:
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
                res = median(l, freq, need=bool)
                q2 = res[0]
                if len(res) == 3: # odd
                        _, pos, miss = res
                        l1 = l[:(pos + 1)]; l2 = l[pos:]
                        freq1 = freq[:(pos + 1)]; freq2 = freq[pos:]
                        freq1[-1] -= (miss + 1); freq2[0] = miss
                        if freq1[-1] == 0:
                                freq1.pop(); l1.pop()
                        if freq2[0] == 0:
                                freq2.pop(0); l2.pop(0)
                        #print(freq1, freq2, sep="\n")
                        q1 = median(l=l1, freq=freq1)
                        q3 = median(l=l2, freq=freq2)
                        return (q1, q2, q3)
                else: # even
                        _, pos1, pos2, k1, k2 = res
                        l1 = l[:(pos1 + 1)]
                        l2 = l[pos2:]
                        freq1 = freq[:(pos1 + 1)]
                        freq2 = freq[pos2:]
                        freq1[-1] = abs((k1) - sum(freq1[:-1])); freq2[0] = abs(sum(freq2[1:]) - (k2))
                        if freq1[-1] == 0:
                                freq1.pop()
                        q1 = median(l=l1, freq=freq1)
                        q3 = median(l=l2, freq=freq2)
                        return q1, q2, q3
        else:
                return tu_phan_vi(l, [1 for _ in l])


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

if __name__ == "__main__":
        a = list(map(eval, """30 32 47 31 32 30 32 29 17 29 32 31""".split()))
        b = list(map(eval, """32 29 32 30 32 31 29 31 32 30 31 29""".split()))
        print(tu_phan_vi(a), tu_phan_vi(b))
