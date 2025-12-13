from process_front_end import *
from collections import Counter

stat_setting(1)
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
                presum_freq = fast(freq)
                pre_s = sum(freq)
                if pre_s % 2 == 0:
                        k = (pre_s // 2)
                        k_ = k + 1
                        pos1 = 0; pos2 = 0
                        for i in presum_freq:
                                if k > i:
                                        pos1 += 1
                                else: break
                        for i_ in presum_freq:
                                if k_ > i_:
                                        pos2 += 1
                                else: break
                        #print(l[pos1], l[pos2])
                        return returning((1/2) * (l[pos1] + l[pos2]))
                else:
                        #print("Running here 3")
                        k = (pre_s - 1) // 2
                        pos = 0
                        for i in presum_freq:
                                if k > i:
                                        pos += 1
                                else: break
                        return returing(l[pos])
        else:
                if choice:
                        #print("Running here 4")
                        freq = [1 for _ in l]
                        import bisect
                        alls = [[k, f] for k, f in filter(l, freq)]
                        alls.sort(key=lambda x: x[0])
                        freq = [i[1] for i in alls]
                        l = [i[0] for i in alls]
                        presum_freq = fast(freq)
                        pre_s = sum(freq)
                        if pre_s % 2 == 0:
                                k = (pre_s // 2)
                                k_ = k + 1
                                pos1 = 0; pos2 = 0
                                for i in presum_freq:
                                        if k > i:
                                                pos1 += 1
                                        else: break
                                for i_ in presum_freq:
                                        if k_ > i_:
                                                pos2 += 1
                                        else: break
                                #print(l[pos1], l[pos2])
                                return returning((1/2) * (l[pos1] + l[pos2]))
                        else:
                                k = (pre_s - 1) // 2
                                pos = 0
                                for i in presum_freq:
                                        if k > i:
                                                pos += 1
                                        else: break
                                return returning(l[pos])
                #print("Running here 5")
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
# min, max

def tu_phan_vi(l: list, freq: list):
        """Idea to fix:
        1. Freq
        2. Zip
        3. DEBUGGING.
        4. CORRECTING
        """
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


def hi(l: list[int], freq: list | None = None):
        new = Counter(l)
        return list(new.most_common(1)[0])[0]

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
               if choice:
                       freq = [1 for _ in l]
                       return mean(l, freq)
               return mean(l)
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
                s = int(s) if s.is_integer() else s
                return s
def do_lech_chuan(l: list[int], freq: list[int] = []):
        return pow(phuong_sai(l, freq), 0.5)

if __name__ == "__main__":
       l = [10, 20, 30]
       freq = [1, 2, 1]
       res = []
       for i, k in zip(l, freq):
               res.extend([i] * k)
       print(res)
       print(median(l, freq))