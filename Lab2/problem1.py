import hashlib
import time
import random

with open("./10-million-password-list-top-1000000.txt") as f:
    password_list = f.read().splitlines()


class Hash:
    def __init__(self, usedforsecurity=False):
        self.count = 0
        self.t = None

    def init(self):
        self.count = 0
        self.t = time.time()

    def hash_password(self, password):
        self.count += 1
        return hashlib.sha1(password.encode(), usedforsecurity=False).hexdigest()


def solve(secret, salt=None, word_count=1):
    h = Hash()
    h.init()
    if word_count > 1:
        while True:
            random.seed(time.time())
            pwd = random.choices(range(999998), k=2)
            password = " ".join([password_list[_] for _ in pwd])
            if h.hash_password(password) == secret:
                return password, time.time() - h.t, h.count

    if salt is not None:
        s = solve(salt)
        for password in password_list:
            if h.hash_password(s[0] + password) == secret:
                return s[0] + password, time.time() - h.t, h.count + s[2]
    else:
        for password in password_list:
            if h.hash_password(password) == secret:
                return password, time.time() - h.t, h.count


if __name__ == '__main__':
    hash_values = [
        "ef0ebbb77298e1fbd81f756a4efc35b977c93dae",
        "0bc2f4f2e1f8944866c2e952a5b59acabd1cebf2",
        "9d6b628c1f81b4795c0266c0f12123c1e09a7ad3",
        "44ac8049dd677cb5bc0ee2aac622a0f42838b34d"
    ]
    print("Hash: ", hash_values[0])
    print("Password: {}\ntime: {}\ntries:{}\n".format(*solve(hash_values[0])))
    print("Hash: ", hash_values[1])
    print("Password: {}\ntime: {}\ntries:{}\n".format(*solve(hash_values[1])))
    print("Hash: ", hash_values[2])
    print("Password: {}\ntime: {}\ntries:{}\n".format(
        *solve(hash_values[2], salt="dfc3e4f0b9b5fb047e9be9fb89016f290d2abb06"))
    )
    print("Hash: ", hash_values[3])
    print("Password: {}\ntime: {}\ntries:{}\n".format(
        *solve(hash_values[3], word_count=2))
    )