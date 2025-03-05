import numpy as np


def ssim(img1: np.ndarray, img2: np.ndarray) -> float:
    """Compute the Structural Similarity Index (SSIM) between two images."""
    # Constants for SSIM
    C1 = (0.01 * 255) ** 2
    C2 = (0.03 * 255) ** 2

    # Compute the mean of the images
    mu_x = np.mean(img1)
    mu_y = np.mean(img2)

    # Compute the variance of the images
    var_x = np.var(img1)
    var_y = np.var(img2)

    # Compute the covariance of the images
    cov_xy = np.cov(img1.flatten(), img2.flatten())[0][1]

    # Compute SSIM
    num = (2 * mu_x * mu_y + C1) * (2 * cov_xy + C2)
    den = (mu_x ** 2 + mu_y ** 2 + C1) * (var_x + var_y + C2)
    return num / den


def psnr(img1: np.ndarray, img2: np.ndarray) -> float:
    """Compute the Peak Signal-to-Noise Ratio (PSNR) between two images."""
    mse = np.mean((img1 - img2) ** 2)
    return 10 * np.log10(255 ** 2 / mse)
