from PIL import Image
import sys
import os
import math


# PSNR = 10xlog10 (MAX^2/MSE)
def getPSNR(stego, cover):
    channels = 3  # hardcoding for rgb images right now
    mse = getMSE(stego, cover)
    max = (channels * 255) ** 2
    if mse == 0:
        return "The Images are Identical"
    psnr = 10 * math.log((max / mse), 10)
    output = "The PSNR is: " + str(psnr) + "\nThe MSE is: " + str(mse)
    return output


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


# status -6 too many args
# status -5 : -4 too few args
# status -3 : -2 overloaded input
# status -1 undefined behavior flag given as image/message
# status 0 nothing happened
# status 1 all good, secret message should be writen to specified file
# status 2 all good, secret message should be printed
def handle_argv(argv):
    status = 0
    stego_path = ""
    cover_path = ""
    unflagged_args = []
    current_flag = ""
    for arg in argv:
        # if there is a current flag & arg is a flag
        if current_flag != "" and arg[0:1] == '-':
            return [-1]
        match arg:
            # flags
            case '--stego':
                current_flag = 'stego image'
            case '-s':
                current_flag = 'stego image'
            case '--cover':
                current_flag = 'cover image'
            case '-c':
                current_flag = 'cover image'
            # input arg
            case _:
                if current_flag != "":
                    match current_flag:
                        case 'stego image':
                            if stego_path != "":
                                return [-2]
                            else:
                                stego_path = arg
                        case 'cover image':
                            if cover_path != "":
                                return [-3]
                            else:
                                status = 1
                                cover_path = arg
                    current_flag = ""
                else:
                    unflagged_args.append(arg)

    # handle unflagged args
    if stego_path == "":
        if len(unflagged_args) > 0:
            stego_path = unflagged_args[0]
            unflagged_args = unflagged_args[1:len(unflagged_args)]
        else:
            return [-4]
    if cover_path == "":
        if len(unflagged_args) > 0:
            status = 1
            cover_path = unflagged_args[0]
            unflagged_args = unflagged_args[1:len(unflagged_args)]
        else:
            return [-5]

    if len(unflagged_args) == 0:
        return [status, stego_path, cover_path]
    else:
        return [-6]

    
def main():
    # python psnr stego cover
    # check that there are 2 arguments
    # check that the dimenstions header info matches
    standardized_argv = handle_argv(sys.argv[1:len(sys.argv)])
    status = standardized_argv[0]
    if status > 0:
        stego_path = standardized_argv[1]
        cover_path = standardized_argv[2]

    match status:
        case -6:
            print("Error, Too Many Arguments Provided")
        case -5:
            print("Error, No Cover Image Provided")
        case -4:
            print("Error, No Stego Image Provided")
        case -3:
            print("Error, Multiple Cover Images Provided")
        case -2:
            print("Error, Multiple Stego Images Provided")
        case -1:
            print("Error, Flag Given as Input to Flag")
        case 1:
            files_exist = True
            if not os.path.isfile(stego_path):
                print("Error, Stego Image Does Not Exist")
                files_exist = False
            if not os.path.isfile(cover_path):
                print("Error, Cover Image Does Not Exist")
                files_exist = False
            if files_exist:
                stego_image = Image.open(stego_path)
                stego_width, stego_height = stego_image.size
                cover_image = Image.open(cover_path)
                cover_width, cover_height = cover_image.size
                if stego_width == cover_width and stego_height == cover_height:
                    print(getPSNR(stego_path, cover_path))
        case _:
            print("Error, Unknown Error")


main()
