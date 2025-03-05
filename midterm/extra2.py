A = "e93ae9c5fc7355d5"
B = "f43afec7e1684adf"

C = int(A, 16) ^ int(B, 16)
print(hex(C)[2:])

f = open("extra2.txt", "w+")

c = [hex(C)[i + 2:i + 4] for i in range(0, len(hex(C)[2:]), 2)]
possible = []
for _ in range(len(c)):
    res = []
    for __ in range(97, 123):
        if 97 <= int(c[_], 16) ^ __ <= 122:
            res.append((chr(__), chr(int(c[_], 16) ^ __)))
    possible.append(res)

a = []
for i in range(len(possible)):
    d = dict()
    for j in range(len(possible[i])):
        d[possible[i][j][0]] = possible[i][j][1]
    a.append(d)
    print(f"Position {i + 1}: {possible[i]}")
    f.write(f"Position {i + 1}: {possible[i]}\n")

words = []
with open("word2.txt", "r") as file:
    for line in file:
        if line != "\n":
            words.append(line.strip().lower())

for word in words:
    if len(word) == len(a):
        flag = True
        for i in range(len(word)):
            if word[i] not in a[i]:
                flag = False
                break
        if flag:
            res = ''.join([a[i][word[i]] for i in range(len(word))])
            print(f"Word: {word} Flag: {res}")

f.close()

a = "security"
b = "networks"

print(f"XOR: {a} ^ {b}")
print(hex(int(a.encode().hex(), 16) ^ int(b.encode().hex(), 16))[2:])

print("pad:")
print(f"XOR: {a} ^ {A}")
print(hex(int(a.encode().hex(), 16) ^ int(A, 16))[2:])
print(f"XOR: {b} ^ {B}")
print(hex(int(b.encode().hex(), 16) ^ int(B, 16))[2:])
