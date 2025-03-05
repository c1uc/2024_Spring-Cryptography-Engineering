import string

ciphers = []
with open("tenciphs.txt", "r") as file:
    for line in file:
        ciphers.append([0] + eval(line.strip()))

ALL_POSSIBILITY = string.printable
ALL_CHAR = string.ascii_letters + string.digits + ",.?!' _{}[]()@#$%^&*+-=<>:;|~`\\\""

prod = 1
f = open("extra2b.txt", "w+")
for i in range(1, len(ciphers[0])):  # m_i
    possible = dict()
    for k in range(256):
        possible[k] = 1

    for pad in range(256):  # pad_i
        for j in range(len(ciphers)):
            k = (pad + ciphers[j][i - 1]) % 256  # k_i = (pad_i + c_i-1) mod 256
            if chr(ciphers[j][i] ^ k) not in ALL_CHAR:  # try m_i = c_i ^ k_i
                possible[pad] = 0
                break

    prod *= sum(possible.values())

    print(f"Position {i}: {' '.join([str(chr(k)) for k, v in possible.items() if v == 1])}")
    f.write(f"Position {i}: {' '.join([str(chr(k)) for k, v in possible.items() if v == 1])}\n")
    # print(f"Position {i}: {''.join([k if k != ' ' else '*SPACE*' for k, v in possible.items() if v == 1])}")
    # f.write(f"Position {i}: {''.join([k if k != ' ' else '*SPACE*' for k, v in possible.items() if v == 1])}\n")
f.close()
print(f"Total possibilities: {prod}")
