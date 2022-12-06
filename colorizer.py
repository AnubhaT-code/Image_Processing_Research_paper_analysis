from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import sys

image10 = Image.open(sys.argv[1]) # size 622*960
image20 = Image.open(sys.argv[2]) # size 156*240
image30 = Image.open(sys.argv[3]) # size 156*240

r = 624
c = 960

image1 = image10.resize((c,r), resample=Image.BOX)
image2 = image20.resize((c,r), resample=Image.BOX)
image3 = image30.resize((c,r), resample=Image.BOX)
# Upsampling Cb4 and Cr4 by 4 times using box filter 

M = [ [ 65.73, 129.05, 25.06 ], [ -37.94, -74.49, 112.43 ], [ 112.43, -94.15, -18.28 ] ]
# Matrix used for conversion as per lecture slides
M = np.array(M)
M = np.multiply(M,1/256) # normalization
M_inv = np.linalg.inv(M) # finding an inverse

def RGBvaluesperpixel(i,j,image1,image2,image3,M):
    # subtraction as per formula
    Y = image1.getpixel((i,j)) - 16
    Cb = image2.getpixel((i,j)) - 128
    Cr = image3.getpixel((i,j)) - 128
            #print(Y,Cb,Cr)
    R = M[0][0]*Y + M[0][1]*Cb + M[0][2]*Cr 
    G = M[1][0]*Y + M[1][1]*Cb + M[1][2]*Cr
    B = M[2][0]*Y + M[2][1]*Cb + M[2][2]*Cr
    # Rounding off to nearest integer
    R = int(R)
    G = int(G)
    B = int(B)
    return((R,G,B))

# image initialization for final image formation
final_image_num = np.full((624, 960, 3), 255, dtype = np.uint8)
final_image = Image.fromarray(final_image_num)

def RGBconvert(image1,image2,image3,final_image,M):
    r,c = final_image.size
    for i in range(r):
        for j in range(c):
            val = RGBvaluesperpixel(i,j,image1,image2,image3,M)
            final_image.putpixel((i, j), val)
    return(final_image)

img = RGBconvert(image1,image2,image3,final_image,M_inv)
img.save("flyingelephant.jpg")