import hashlib
import time


def md5(file):
    return hashlib.md5(file).hexdigest()


def sha1(file):
    return hashlib.sha1(file).hexdigest()


def sha224(file):
    return hashlib.sha224(file).hexdigest()


def sha256(file):
    return hashlib.sha256(file).hexdigest()


def sha512(file):
    return hashlib.sha512(file).hexdigest()


def sha3_224(file):
    return hashlib.sha3_224(file).hexdigest()


def sha3_256(file):
    return hashlib.sha3_256(file).hexdigest()


def sha3_512(file):
    return hashlib.sha3_512(file).hexdigest()


def checksum(filename, hash_function):
    with open(filename, 'rb') as f:
        t = time.time()
        hashed = hash_function(f.read())
        return hashed, time.time() - t


def main():
    res = [
        (checksum("./BigBuckBunny.mp4", md5)[::-1], "md5"),
        (checksum("./BigBuckBunny.mp4", sha1)[::-1], "sha1"),
        (checksum("./BigBuckBunny.mp4", sha224)[::-1], "sha224"),
        (checksum("./BigBuckBunny.mp4", sha256)[::-1], "sha256"),
        (checksum("./BigBuckBunny.mp4", sha512)[::-1], "sha512"),
        (checksum("./BigBuckBunny.mp4", sha3_224)[::-1], "sha3_224"),
        (checksum("./BigBuckBunny.mp4", sha3_256)[::-1], "sha3_256"),
        (checksum("./BigBuckBunny.mp4", sha3_512)[::-1], "sha3_512")
    ]
    print("-" * 10 + "res" + "-" * 10)
    [print("type: {}\ntime: {}\nchecksum:{}\n\n".format(_[1], *_[0])) for _ in res]
    print("-" * 10 + "rank" + "-" * 10)
    res = sorted(res, key=lambda x: x[0][0])
    [print("type: {}\ntime: {}\nchecksum:{}\n\n".format(_[1], *_[0])) for _ in res]


if __name__ == '__main__':
    main()
