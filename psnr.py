from PIL import Image
import sys
import os
import math


# PSNR = 10xlog10 (MAX^2/MSE)
def getPSNR(stego, cover):
    channels = 3 # hardcoding for rgb images right now
    mse = getMSE(stego, cover)
    max = (channels * 255) ** 2
    if mse == 0:
        return "The Images are Identical"
    psnr = 10 * math.log((max / mse), 10)
    return psnr


def getMSE(stego, cover):
    cover_img = Image.open(cover)
    cover_pix = cover_img.load()

    stego_img = Image.open(stego)
    stego_pix = stego_img.load()

    width, height = cover_img.size

    sum = 0
    for x in range(width):
        for y in range(height):
            sum += (getInten(stego_pix[x, y]) - getInten(cover_pix[x, y])) ** 2

    return (sum / (width * height))


def getInten(pixel):
    sum = 0
    for channel in pixel:
        sum += channel
    return sum


def main():
    # python psnr stego cover
    # check that there are 2 arguments
    stego = sys.argv[-2]
    cover = sys.argv[-1]
    # check that the dimenstions header info matches

    print(getPSNR(stego, cover))


main()






