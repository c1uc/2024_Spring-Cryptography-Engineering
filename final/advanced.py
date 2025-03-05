import os
import random
import numpy as np
import cv2
import matplotlib.pyplot as plt


WHT_4 = np.array([[1, 1, 1, 1], [1, -1, 1, -1], [1, 1, -1, -1], [1, -1, -1, 1]])


class Watermarking:
    def __init__(self, key):
        self.n = None
        self.key = key
        self.permutation: np.ndarray
        self.inverse_permutation: np.ndarray

    def _generate_permutation(self, n: int) -> None:
        """Generate a permutation of n elements based on the given key."""
        random.seed(self.key)
        permutation = list(range(n))
        random.shuffle(permutation)
        self.permutation = np.asarray(permutation)

        inverse = np.zeros(n, dtype=int)
        for i, p in enumerate(permutation):
            inverse[p] = i
        self.inverse_permutation = inverse

    def _shuffle_bits(self, data: np.ndarray) -> np.ndarray:
        """Shuffle bits of data according to the given permutation."""
        shuffled_data = np.zeros_like(data, dtype=int)
        for i, p in enumerate(self.permutation):
            shuffled_data[p] = data[i]
        return shuffled_data

    def _reconstruct_bits(self, shuffled_data: np.ndarray) -> np.ndarray:
        """Reconstruct the original bit sequence from the shuffled data using the inverse permutation."""
        n = len(self.inverse_permutation)
        original_data = np.zeros(n, dtype=int)
        for i, p in enumerate(self.inverse_permutation):
            original_data[p] = shuffled_data[i]
        return original_data

    @staticmethod
    def _convert_to_binary(image: np.ndarray) -> np.ndarray:
        return np.unpackbits(image)

    @staticmethod
    def _wht(data: np.ndarray) -> np.ndarray:
        return 0.25 * WHT_4 @ data

    @staticmethod
    def _inverse_wht(data: np.ndarray) -> np.ndarray:
        return WHT_4 @ data

    def _augment_wht(self, data: np.ndarray, bits: np.ndarray) -> np.ndarray:
        wht = self._wht(data)
        dist = np.abs(np.floor(wht[2]) - np.floor(wht[3]))
        avg = (np.floor(wht[2]) + np.floor(wht[3])) / 2

        fst = np.zeros(4)
        snd = np.zeros(4)

        for i in range(4):
            if dist[i] % 2 == 0:
                if bits[i] == 0:
                    fst[i] = avg[i] - dist[i]
                    snd[i] = avg[i] + dist[i]
                else:
                    fst[i] = avg[i] - (dist[i] / 2 - 0.5)
                    snd[i] = avg[i] + (dist[i] / 2 - 0.5)
            else:
                if bits[i] == 0:
                    fst[i] = avg[i] - (dist[i] / 2 - 0.5)
                    snd[i] = avg[i] + (dist[i] / 2 - 0.5)
                else:
                    fst[i] = avg[i] - dist[i] / 2
                    snd[i] = avg[i] + dist[i] / 2

        high = np.max([fst, snd], axis=0)
        low = np.min([fst, snd], axis=0)

        e_2 = np.where(wht[2] < wht[3], low, high)
        e_3 = np.where(wht[3] <= wht[2], low, high)
        wht = np.array([wht[0], wht[1], e_2, e_3])
        return self._inverse_wht(wht).astype(int)

    def _extract_bits(self, data: np.ndarray) -> np.ndarray:
        wht = self._wht(data)
        dist = np.abs(wht[2] - wht[3])
        bits = np.mod(np.floor(dist), 2)
        return bits.astype(int)

    def _split_and_augment(self, image: np.ndarray, bits: np.ndarray) -> np.ndarray:
        """split the data into 4x4 blocks and augment each block with the watermark."""
        n, m = image.shape[:2]
        augmented_data = np.zeros_like(image)
        idx = 0
        for c in range(image.shape[2]):
            for i in range(0, n, 4):
                for j in range(0, m, 4):
                    block = image[i:i + 4, j:j + 4, c]
                    if idx >= len(bits):
                        augmented_data[i:i + 4, j:j + 4, c] = block
                        continue
                    block = self._augment_wht(block, bits[idx:idx + 4])
                    augmented_data[i:i + 4, j:j + 4, c] = block
                    idx += 4
        return augmented_data

    def embed(self, image: np.ndarray, watermark: np.ndarray) -> np.ndarray:
        watermark = self._convert_to_binary(watermark)

        n = image.shape[0] * image.shape[1] * image.shape[2] // 4
        self.n = len(watermark)
        watermark = np.pad(watermark, (0, n - len(watermark)), mode='constant')
        self._generate_permutation(n)

        watermark = self._shuffle_bits(watermark)
        image = self._split_and_augment(image, watermark)
        return image

    def extract(self, image: np.ndarray) -> np.ndarray:
        n, m = image.shape[:2]
        watermark = []
        for c in range(image.shape[2]):
            for i in range(0, n, 4):
                for j in range(0, m, 4):
                    block = image[i:i + 4, j:j + 4, c]
                    watermark += self._extract_bits(block).tolist()
        watermark = self._reconstruct_bits(np.asarray(watermark))[:self.n]
        w = np.sqrt(self.n / 24).astype(int)
        return np.packbits(watermark).reshape(w, w, 3)

    def show_results(self, image: str, watermark: str, to_jpg=False) -> None:
        cover = cv2.imread(image)
        h, w = cover.shape[:2]
        cover = cv2.resize(cover, (cover.shape[1] - w % 4, cover.shape[0] - h % 4), interpolation=cv2.INTER_AREA)
        h, w = cover.shape[:2]
        max_size = np.sqrt(h * w / 32).astype(int)
        secret = cv2.imread(watermark)
        secret = cv2.resize(secret, (max_size, max_size), interpolation=cv2.INTER_AREA)

        cv2.imwrite(f"{image[:-4]}_WHT_resized_secret.png", secret)
        cv2.imwrite(f"{image[:-4]}_WHT_resized_cover.png", cover)

        watermarked_image = self.embed(cover, secret)
        if to_jpg:
            cv2.imwrite(f"{image[:-4]}_jpg_WHT_watermarked.jpg", watermarked_image)
            watermarked_image = cv2.imread(f"{image[:-4]}_jpg_WHT_watermarked.jpg")
        else:
            cv2.imwrite(f"{image[:-4]}_png_WHT_watermarked.png", watermarked_image)
            watermarked_image = cv2.imread(f"{image[:-4]}_png_WHT_watermarked.png")

        extracted_watermark = self.extract(watermarked_image)

        cv2.imwrite(f"{image[:-4]}_WHT_extracted.png", extracted_watermark)
        plt.figure(figsize=(10, 10))
        plt.subplot(2, 2, 1)
        plt.imshow(cv2.cvtColor(cover, cv2.COLOR_BGR2RGB))
        plt.title('Original Image')
        plt.axis('off')
        plt.subplot(2, 2, 2)
        plt.imshow(cv2.cvtColor(secret, cv2.COLOR_BGR2RGB))
        plt.title('Original Watermark')
        plt.axis('off')
        plt.subplot(2, 2, 3)
        plt.imshow(cv2.cvtColor(watermarked_image, cv2.COLOR_BGR2RGB))
        plt.title('Watermarked Image')
        plt.axis('off')
        plt.subplot(2, 2, 4)
        plt.imshow(cv2.cvtColor(extracted_watermark, cv2.COLOR_BGR2RGB))
        plt.title('Extracted Watermark')
        plt.axis('off')
        i = 0
        while True:
            if not (f"{image[:-4]}_WHT_results.png" in os.listdir()):
                i += 1
                if i == 100:
                    break
            else:
                break
        plt.tight_layout()
        plt.savefig(f"{image[:-4]}_WHT_results.png")
        plt.show()


def main():
    # cover: 512x512x3
    # secret: 90x90x3
    key = 'flag_t34m_n4me_1s_3ncrypt3d'
    watermarking = Watermarking(key)
    for _ in range(1, 2):
        watermarking.show_results(f'cover_{_}.png', 'secret.png', to_jpg=False)


if __name__ == '__main__':
    main()
