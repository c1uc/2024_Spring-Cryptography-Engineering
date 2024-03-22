import argparse
import string

class Problem1:
    def __init__(self):
        pass

    CIPHER = """
    C UYGHARMZ IUWMPRWIR GAIR YVRMP
    MBHMZWMPUM C VMMXWPE YV PYR VCZ
    ZMGYQMD VZYG CXCZG YP CPCXKTWPE CPD MBHXYZM
    RNM VXYYD YV CDQCPUMD OPYSXMDEM SNWUN MCUN
    KMCZ LZWPEI SWRN WR
    """

    def freq(self):
        freq = {}
        for c in string.ascii_uppercase:
            freq[c] = 0
        for c in self.CIPHER:
            if c.isalpha():
                if c in freq:
                    freq[c] += 1
        return freq

    def decrypt(self):
        s = string.ascii_uppercase
        func = lambda x: s[(3*s.index(x) + 20) % 26] if x.isalpha() else x
        return ''.join(map(func, self.CIPHER))


class Problem2:
    def __init__(self):
        pass

    N = 30

    def inverse(self, a):
        for i in range(self.N):
            if (a*i) % self.N == 1:
                return i
        return None

    def inverse_pairs(self):
        return [(i, self.inverse(i)) for i in range(self.N) if self.inverse(i) is not None]

    def eval(self, x, a, b):
        return (a*x + b) % self.N


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Problem 1')
    parser.add_argument('-1f', '--freq', action='store_true', help='Frequency of characters')
    parser.add_argument('-1d', '--decrypt', action='store_true', help='Decrypt the cipher')
    parser.add_argument('-2b', '--problem2b', action='store_true', help='Problem 2')
    parser.add_argument('-2c', '--problem2c', action='store_true', help='Problem 2')
    args = parser.parse_args()
    p1 = Problem1()
    p2 = Problem2()
    if args.freq:
        print(p1.freq())
    elif args.decrypt:
        print(p1.decrypt())
    elif args.problem2b:
        print(p2.inverse_pairs())
    elif args.problem2c:
        xs = [4, 10, 27]
        ys = [8, 26, 7]
        ps = p2.inverse_pairs()
        b = 0
        for p in ps:
            a = p[0]
            rs = [p2.eval(x, a, b) for x in xs]
            if (rs[0] - rs[1] == 12 or rs[1] - rs[0] == 18) and (rs[1] - rs[2] == 19 or rs[2] - rs[1] == 11):
                print(f"a: {a}, b: {b}")
                print(rs)
                break
    else:
        print("No option selected")

