PLAINTEXT = """ATNYCUWEARESTRIVINGTOBEAGREATUNIVERSITYTHATTRANSCENDSDISCIPLINARYDIVIDESTOSOLVETHEINCREASINGLYCOMPLEXPROBLEMSTHATTHEWORLDFACESWEWILLCONTINUETOBEGUIDEDBYTHEIDEATHATWECANACHIEVESOMETHINGMUCHGREATERTOGETHERTHANWECANINDIVIDUALLYAFTERALLTHATWASTHEIDEATHATLEDTOTHECREATIONOFOURUNIVERSITYINTHEFIRSTPLACE"""


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


def shift_and_mod(x: list, p: list):
    x = shift(x)
    x = mod(x, p)
    return x


def encrypt(plaintext: str, poly: list, x: list):
    ciphertext = ""
    for _ in plaintext:
        ciphertext += bin(ord(_) ^ convolution(x))[2:].zfill(8)
        x = shift_and_mod(x, poly)
    return ciphertext


def decrypt(ciphertext: str, poly: list, x: list):
    plaintext = ""
    for i in range(0, len(ciphertext), 8):
        plaintext += chr(int(ciphertext[i:i + 8], 2) ^ convolution(x))
        x = shift_and_mod(x, poly)
    return plaintext


def brute_crack(ciphertext: str):
    for i in range(1, 2 ** 9):
        x = [int(_) for _ in bin(i)[2:].zfill(8)]
        ok = True
        for _ in range(len(ciphertext) - 8):
            a_n = int(ciphertext[_], 2)
            b_n = [int(_) for _ in ciphertext[_ + 1:_ + 9]]

            res = 0
            for j in range(8):
                res += x[j] * b_n[j]
            res = res % 2
            if res != a_n:
                ok = False
                break

        if ok:
            print(f"Found x: {x}")
            break
        else:
            continue


def main():
    plaintext = PLAINTEXT

    poly = [1, 0, 0, 0, 1, 1, 1, 0, 1]
    x = [0, 0, 0, 0, 0, 0, 0, 1]

    ciphertext = encrypt(plaintext, poly, x)
    print(f"Ciphertext:\n{ciphertext}\n\n")
    # [print(ciphertext[i:i + 8]) for i in range(0, len(ciphertext), 8)]

    decrypted = decrypt(ciphertext, poly, x)
    print(f"Decrypted:\n{decrypted}\n\n")

    print(f"Plaintext == Decrypted: {plaintext == decrypted}\n\n")

    tmp = ciphertext[::8]
    brute_crack(tmp)


if __name__ == "__main__":
    main()
