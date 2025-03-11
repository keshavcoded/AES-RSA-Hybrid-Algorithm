from math import log10, sqrt
import cv2
import numpy as np

def PSNR(original,reconstructed):
    mse = np.mean((original - reconstructed) ** 2)
    print(mse)
    if mse == 0: 
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

original = cv2.imread("D:\\2.jpeg")
reconstructed = cv2.imread("D:\\DEC.jpg")
value = PSNR(original,reconstructed)
print(f"PSNR value is {value} dB")
