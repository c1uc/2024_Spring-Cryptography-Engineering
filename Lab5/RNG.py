import random
from Crypto.Cipher import AES


def unsecure_random_number(f):
    for _ in range(1024 * 1024):
        f.write(bytes([random.randint(0, 255)]))


def configure_aes():
    key = b'starburst_stream'
    iv = b'chihayaanontokyo'
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes


def secure_random_number(f):
    aes = configure_aes()
    for _ in range(65536):
        f.write(aes.encrypt(bytes([random.randint(0, 255) for _ in range(16)])))


def generate_system_random_number(f):
    rng = random.SystemRandom()
    for _ in range(1024 * 1024):
        f.write(bytes([rng.randint(0, 255)]))


def main(func):
    with open('random.bin', 'wb') as f:
        func(f)


if __name__ == '__main__':
    # [unsecure_random_number, secure_random_number, generate_system_random_number]
    main(unsecure_random_number)
