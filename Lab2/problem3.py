import numpy as np
import argparse

cipher = "UONCSVAIHGEPAAHIGIRLBIECSTECSWPNITETIENOIEEFDOWECXTRSRXSTTARTLODYFSOVNEOECOHENIODAARQNAELAFSGNOPTE"


def get_vowel_count(s):
    vowels = ['A', 'E', 'I', 'O', 'U']
    vowel_count = 0
    for c in s:
        if c in vowels:
            vowel_count += 1
    return vowel_count


def get_diff():
    divisor = [7, 14]
    for d in divisor:
        s = 0
        print(f"shape: {d}x{len(cipher) // d}")
        for i in range(d):
            diff = np.abs(get_vowel_count(cipher[i::d]) - 0.4 * len(cipher[i::d]))
            s += diff
            print(cipher[i::d], "Vowel Count:", get_vowel_count(cipher[i::d]),
                  f"diff: {diff}")
        print(f"Average of diff: {s / d}")
        print()


def permute():
    perm = [4, 1, 5, 6, 0, 3, 2]
    shape = (7, 14)
    words = np.array(list(cipher)).reshape(shape).T
    for w in words:
        print("".join(w[perm]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--diff", help="calculate the diff", action="store_true")
    parser.add_argument("-p", "--permute", help="permute the words", action="store_true")
    args = parser.parse_args()
    if args.diff:
        get_diff()
    if args.permute:
        permute()
