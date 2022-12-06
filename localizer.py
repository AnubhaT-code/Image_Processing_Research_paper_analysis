from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import sys

image = Image.open(sys.argv[1])

def meanvaluebr(image):
    
    meanbr = 0.0
    dim = image.size
    prod = dim[0]*dim[1]
    
    for i in range(0,dim[0]):
        for j in range(0,dim[1]):
            R,G,B = image.getpixel((i,j))
            meanbr += abs(R-B)
    
    meanbrd = meanbr/ prod
    return (meanbrd)      

def meanvaluerg(image):
    meanrg = 0.0
    dim = image.size
    prod = dim[0]*dim[1]
    
    for i in range(0,dim[0]):
        for j in range(0,dim[1]):
            R,G,B = image.getpixel((i,j))
            meanrg += abs(R-G)
    
    meanrgd = meanrg/prod
    return(meanrgd)        

def meanvaluebg(image,low,high):
    meangb = 0.0
    dim = image.size
    prod = dim[0]*dim[1]
    c = 0
    for i in range(0,dim[0]):
        for j in range(0,dim[1]):
            R,G,B = image.getpixel((i,j))
            if abs(B-G) >= low and abs(B-G) <= high :
                meangb += abs(B-G)
            else:
                c = c + 1
    prod -= c 
    meangbd = meangb/prod
    return(meangbd)
    
def meanvaluecalcdiff(image,low,high):
    calcdiff = 0.0
    dim = image.size
    prod = dim[0]*dim[1]
    c = 0
    for i in range(0,dim[0]):
        for j in range(0,dim[1]):
            R,G,B = image.getpixel((i,j))
            if abs(2*G-R-B) >= low and abs(2*G-R-B) <= high :
                calcdiff += abs(2*G-R-B)
            else:
                c = c + 1
    prod -= c 
    calcdiffd = calcdiff/prod
    return(calcdiffd)

def isRoad(image):
    meanrgd = meanvaluerg(image)
    meanbrd = meanvaluebr(image)
    meangbd = meanvaluebg(image,7,20)
    calcdiffd = meanvaluecalcdiff(image,0,12)
    
    c = 0
    if meanrgd > 13.0:
        c = c + 1
    if meanbrd > 24.0:
        c = c + 1
    if meangbd > 8.0 and meangbd < 25.0:
        c = c + 1
    if calcdiffd > 3.7 and calcdiffd < 8.0:
        c = c + 1
    if c == 4:
        return True
    else:
        return False

def isBuilding(image):
    meanrgd = meanvaluerg(image)
    meanbrd = meanvaluebr(image)
    meangbd = meanvaluebg(image,0,6)
    calcdiffd = meanvaluecalcdiff(image,1,8)
    
    c = 0
    if meanrgd < 10.0 and meanrgd > 2.0:
        c = c + 1
    if meanbrd > 3.0 and meanbrd < 17:
        c = c + 1
    if meangbd < 8.0:
        c = c + 1
    if calcdiffd < 3.8:
        c = c + 1
    if c == 4:
        return True
    else:
        return False

def isGrass(image):
    meanrgd = meanvaluerg(image)
    meanbrd = meanvaluebr(image)
    meangbd = meanvaluebg(image,0,80)
    calcdiffd = meanvaluecalcdiff(image,12,85)
    
    c = 0
    if meanrgd > 10.0 and meanrgd < 14.0:
        c = c + 1
    if meanbrd < 26.0 and meanbrd > 15.0:
        c = c + 1
    if meangbd > 25.0:
        c = c + 1
    if calcdiffd > 35.0:
        c = c + 1
    if c == 4:
        return True
    else:
        return False

if(isBuilding(image)):
    print(1)
if(isGrass(image)):
    print(2)
if(isRoad(image)):
    print(3)

