#from process_front_end import *
from collections import Counter

#stat_setting(1)
#choice = dict_of_setting["Statistics"]
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
        #global choice
        choice = 1
        if freq:
                n = len(l)
                if choice == 0:
                        print("Running here 1")
                        #freq = None
                        l = sorted(l)
                        n = len(l)
                        if n % 2 == 0:
                                k = n // 2
                                res = (1/2) * (l[k - 1] + l[k])
                                res = (res)
                                return res
                        else:
                                k = (n - 1) // 2
                                return (l[k])
                # Check the length of the list 'frequency'
                print("Running here 2")
                import bisect
                alls = [(k, f) for k, f in filter(l, freq)]
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
                        print(l[pos1]), l[pos2]
                        return (1/2) * (l[pos1] + l[pos2])
                else:
                        print("Running here 3")
                        k = (pre_s - 1) // 2
                        pos = 0
                        for i in freq:
                                k -= i
                                if k < 0:
                                        break
                                pos += 1
                        return l[pos]
        else:
                if choice:
                        print("Running here 4")
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
                                pos1 = bisect.bisect_right(presum_freq, k)
                                pos2 = bisect.bisect_right(presum_freq, k_)
                                return (1/2) * (l[pos1] + l[pos2])
                        else:
                                k = (pre_s - 1) // 2
                                pos = bisect.bisect_right(presum_freq, k)
                                return l[pos]
                print("Running here 5")
                l = sorted(l)
                n = len(l)
                if n % 2 == 0:
                        k = n // 2
                        res = (1/2) * (l[k - 1] + l[k])
                        res = (res)
                        return res
                else:
                        k = (n - 1) // 2
                        return (l[k])
if __name__ == "__main__":
       l = [25, 26, 27, 29, 31, 34]
       freq = [4, 7, 8, 3, 1, 1]
       print(median(l, freq))