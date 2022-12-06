import numpy as np
from PIL import Image
import cv2
import sys
import math
import cv2

def dist_calculate(x, y, p, q):
    return np.sqrt((x-p)**2 + (y-q)**2)


def gaussian_calculate(x, sig):
    return (1.0 / (2 * 3.14 * (sig ** 2))) * math.exp(- (x ** 2) / (2 * sig ** 2))


def apply_bilateral_filter_per_pixel(input_image, out_image, x, y, d, sig_i, sig_s):
    r = d//2
    row = len(input_image)
    col = len(input_image[0])
    filt = 0
    Wp = 0
    i = 0
    while i < d:
        j = 0
        while j < d:
            p = x - (r - i)
            q = y - (r - j)
            if p >= row:
                np -= row
            if q >= col:
                q -= col
            gi = gaussian_calculate(input_image[p][q] - input_image[x][y], sig_i)
            gs = gaussian_calculate(dist_calculate(p, q, x, y), sig_s)
            w = gi * gs
            filt += input_image[p][q] * w
            Wp += w
            j += 1
        i += 1
    filt = filt / Wp
    out_image[x][y] = int(round(filt))


def bilateral_filter_own(input_image, d, sig_i, sig_s):
    out_image = np.zeros(input_image.shape)
    row = len(input_image)
    col = len(input_image[0])
    i = 0
    while i < row:
        j = 0
        while j < col:
            apply_bilateral_filter_per_pixel(input_image, out_image, i, j, d, sig_i, sig_s)
            j += 1
        i += 1
    return out_image



# Read the image.
img = cv2.imread(sys.argv[1])

# Apply bilateral filter with d = 15,
# sigmaColor = sigmaSpace = 75.

gaussian = cv2.GaussianBlur(img,(5,5),0)
bilateral = cv2.bilateralFilter(gaussian, 45, 75, 75)
# new_img = bilateral_filter_own(img, 45, 75, 75)
# Save the output.
cv2.imwrite('denoised.jpg', bilateral)






