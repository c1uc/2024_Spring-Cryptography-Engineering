import numpy as np
from PIL import Image
import sklearn
import scipy


class ImageQR:
    def __init__(self, alpha=0.01):
        self.alpha = alpha
        self.q_c = None
        self.r_c = None
        self.q_s = None

    @staticmethod
    def qr_decompose(image: np.ndarray):
        qs = []
        rs = []
        for i in range(3):
            q, r = scipy.linalg.qr(image[:, :, i], mode='full', pivoting=False)
            qs.append(q)
            rs.append(r)

        return np.dstack(qs), np.dstack(rs)

    @staticmethod
    def qr_compose(q: np.ndarray, r: np.ndarray):
        assert q.shape[2] == 3
        assert r.shape[2] == 3
        image = np.zeros_like(r)
        for i in range(3):
            image[:, :, i] = q[:, :, i] @ r[:, :, i]
        return image

    def encode_qr(self, cover_image: Image.Image, secret_image: Image.Image):
        cover_image = np.array(cover_image)
        secret_image = np.array(secret_image)
        secret_image = np.pad(secret_image, ((0, cover_image.shape[0] - secret_image.shape[0]),
                                             (0, cover_image.shape[1] - secret_image.shape[1]),
                                             (0, 0)))

        q_c, r_c = self.qr_decompose(cover_image)
        q_s, r_s = self.qr_decompose(secret_image)
        self.q_c = q_c
        self.r_c = r_c
        self.q_s = q_s

        res = self.qr_compose(q_c, r_c + self.alpha * r_s).round().astype(np.uint8)

        return Image.fromarray(res)

    def decode_qr(self, stego_image: Image.Image):
        stego_image = np.array(stego_image)
        q_c_t = np.dstack([self.q_c[:, :, i].T for i in range(3)])
        r_r = self.qr_compose(q_c_t, stego_image)

        res = self.qr_compose(self.q_s, (r_r - self.r_c) / self.alpha).round().astype(np.uint8)

        return Image.fromarray(res)


def test(image1, image2):
    def compose(q, r):
        assert q.shape[2] == 3
        assert r.shape[2] == 3
        res = np.zeros_like(r)
        for i in range(3):
            res[:, :, i] = q[:, :, i] @ r[:, :, i]

        return res

    def decompose(arr):
        qs = []
        rs = []
        for i in range(3):
            q, r = scipy.linalg.qr(arr[:, :, i], mode='full', pivoting=False)
            qs.append(q)
            rs.append(r)
        return np.dstack(qs), np.dstack(rs)

    cover_image = Image.open(image2)
    arr1 = np.array(cover_image)

    secret_image = Image.open(image1)
    arr2 = np.array(secret_image)

    arr2 = np.pad(arr2, ((0, arr1.shape[0] - arr2.shape[0]),
                         (0, arr1.shape[1] - arr2.shape[1]),
                         (0, 0)))

    q_1, r_1 = decompose(arr1)
    q_2, r_2 = decompose(arr2)

    assert np.allclose(arr1, compose(q_1, r_1), atol=1)
    assert np.allclose(arr2, compose(q_2, r_2), atol=1)

    arr3 = compose(q_1, r_1 + 0.1 * r_2)
    r_3 = compose(np.dstack([q_1[:, :, i].T for i in range(3)]), arr3)

    assert np.allclose(arr3, compose(q_1, r_3), atol=1)

    arr4 = compose(q_2, r_3 - r_1)

    assert np.allclose((r_3 - r_1) / 0.1, r_2, atol=1)
    assert np.allclose(arr4, arr2, atol=1)

    print("Test passed")


def test1():
    arr1 = np.random.rand(100, 100)
    arr2 = np.random.rand(100, 100)

    q_1, r_1 = scipy.linalg.qr(arr1, mode='full', pivoting=False)
    q_2, r_2 = scipy.linalg.qr(arr2, mode='full', pivoting=False)

    assert np.allclose(arr1, q_1 @ r_1)
    assert np.allclose(arr2, q_2 @ r_2)

    arr3 = q_1 @ (r_1 + r_2)
    r_3 = q_1.T @ arr3

    arr4 = q_2 @ (r_3 - r_1)

    assert np.allclose(r_3 - r_1, r_2)
    assert np.allclose(arr4, arr2)

    print("Test passed")


def test2():
    def compose(q, r):
        assert q.shape[2] == 3
        assert r.shape[2] == 3
        res = np.zeros_like(r)
        for i in range(3):
            res[:, :, i] = q[:, :, i] @ r[:, :, i]
        return res

    def decompose(arr):
        qs = []
        rs = []
        for i in range(3):
            q, r = scipy.linalg.qr(arr[:, :, i], mode='full', pivoting=False)
            qs.append(q)
            rs.append(r)
        return np.dstack(qs), np.dstack(rs)

    arr1 = np.random.rand(100, 100, 3)
    arr2 = np.random.rand(100, 100, 3)

    q_1, r_1 = decompose(arr1)
    q_2, r_2 = decompose(arr2)

    assert np.allclose(arr1, compose(q_1, r_1))
    assert np.allclose(arr2, compose(q_2, r_2))

    arr3 = compose(q_1, r_1 + r_2)
    r_3 = compose(np.dstack([q_1[:, :, i].T for i in range(3)]), arr3)

    assert np.allclose(arr3, compose(q_1, r_3))

    arr4 = compose(q_2, r_3 - r_1)

    assert np.allclose(r_3 - r_1, r_2)
    assert np.allclose(arr4, arr2)

    print("Test passed")


def enc_and_dec(image1, image2):
    secret_image = Image.open(image1)
    cover_image = Image.open(image2)
    assert np.all(np.asarray(secret_image.size) <= np.asarray(cover_image.size))
    qr = ImageQR()

    stego_image = qr.encode_qr(cover_image, secret_image)
    stego_image.save("stego.png")

    decoded_image = qr.decode_qr(stego_image)
    decoded_image.save("decoded.png")
    pass


if __name__ == "__main__":
    # test1()
    # test2()
    # test("secret.png", "cover.png")
    enc_and_dec("secret.png", "cover.png")
