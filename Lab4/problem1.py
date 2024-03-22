def convolution(x: list):
    fact = 1
    res = 0
    for i in range(len(x) - 1, -1, -1):
        res += x[i] * fact
        fact *= 2
    return res


def shift(x: list):
    return x + [0]


def mod(x: list, p: list):
    while len(x) >= len(p):
        x = [x[i] ^ p[i] for i in range(len(p))] + x[len(p):]
        while x[0] == 0 and len(x) > 1:
            x = x[1:]
    return x


def main():
    poly = [1, 0, 0, 0, 1, 1, 1, 0, 1]
    x = [0, 0, 0, 0, 0, 0, 0, 1]
    record = [1 for _ in range(2 ** len(poly) - 1)]
    count = 0
    while record[convolution(x)] == 1:
        count += 1
        print(count, x)
        record[convolution(x)] = 0
        x = shift(x)
        x = mod(x, poly)

    print(f"The period of the sequence {poly} is {count}")


if __name__ == "__main__":
    main()
