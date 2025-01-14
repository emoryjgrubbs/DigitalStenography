from PIL import Image
from PIL import UnidentifiedImageError
import sys
import os


def modify_image_string(input_image_path, output_image_path, binary_message):
    # variables
    image = Image.open(input_image_path)
    pixels = image.load()

    width, height = image.size

    if type(pixels[0, 0]) is tuple:
        color_channels = len(pixels[0, 0])
    else:
        color_channels = 1

    img_x = 0
    img_y = 0
    lsb_color = 0  # 0 = red, 1 = green, 2 = blue
    lsb_bit = 0  # 2^lsb_bit is what gets modified

    image = Image.open(input_image_path)
    pixels = image.load()

    width, height = image.size

    binary_message += '1111111111111110'  # End of message delimiter

    # modify pixels with image data
    for message_index in range(len(binary_message)):
        image.putpixel((img_x, img_y),  modify_pixel(pixels[img_x, img_y], binary_message[message_index], lsb_color, lsb_bit))
        img_x += 1
        if img_x == width:
            img_x = 0
            img_y += 1
            if img_y == height:
                img_y = 0
                lsb_color += 1
                if lsb_color == color_channels:
                    lsb_color = 0
                    lsb_bit += 1
                    # ABORT
                    if lsb_bit == 8:
                        return -1

    # ending clean up/saving
    image.save(output_image_path)
    return 0


def modify_image_txt(input_image_path, output_image_path, message_file_path):
    # variables
    get_eof = open(message_file_path, "a")
    eof = get_eof.tell()
    get_eof.close()
    message_text = open(message_file_path, 'r')
    image = Image.open(input_image_path)
    pixels = image.load()

    width, height = image.size

    if type(pixels[0, 0]) is tuple:
        color_channels = len(pixels[0, 0])
    else:
        color_channels = 1

    img_x = 0
    img_y = 0
    lsb_color = 0  # 0 = red, 1 = green, 2 = blue
    lsb_bit = 0  # 2^lsb_bit is what gets modified

    file_index = 0

    # loop through 512 byte chunks of text data, until file_index + 512 > eof
    while file_index + 512 < eof:
        # read data
        message_chunk = message_text.read(512)
        binary_message_chunk = text_to_binary(message_chunk)
        # modify pixels with image data
        for chunk_index in range(len(binary_message_chunk)):
            image.putpixel((img_x, img_y),  modify_pixel(pixels[img_x, img_y], binary_message[message_index], lsb_color, lsb_bit))
            img_x += 1
            if img_x == width:
                img_x = 0
                img_y += 1
                if img_y == height:
                    img_y = 0
                    lsb_color += 1
                    if lsb_color == color_channels:
                        lsb_color = 0
                        lsb_bit += 1
                        # if lsb_bit == 8, the all bit of all colors of all pixels modified, ABORT
                        if lsb_bit == 8:
                            return -1
        file_index += 512

    # do a final pass with the remaining bytes, appending the ending delimiter
    # read data
    message_chunk = message_text.read(eof - file_index)
    binary_message_chunk = text_to_binary(message_chunk)
    binary_message_chunk += '1111111111111110'  # End of message delimiter
    # modify pixels with image data
    for chunk_index in range(len(binary_message_chunk)):
        pixels[img_x, img_y] = modify_pixel(pixels[img_x, img_y], binary_message_chunk[chunk_index], lsb_color, lsb_bit)
        img_x += 1
        if img_x == width:
            img_x = 0
            img_y += 1
            if img_y == height:
                img_y = 0
                lsb_color += 1
                if lsb_color == color_channels:
                    lsb_color = 0
                    lsb_bit += 1
                    # ABORT
                    if lsb_bit == 8:
                        return -1

    # ending clean up/saving
    image.save(output_image_path)
    message_text.close()
    return 0


def modify_pixel(old_pixel, data, color_channel, modify_bit):
    # shift data to lowest unmodified bit
    shifted_data = int(data) << modify_bit
    filter = 2 ** modify_bit

    # Modify the current least significant bit of the current color channel
    if type(old_pixel) is tuple:
        new_pixel = list(old_pixel)
        new_pixel[color_channel] = (old_pixel[color_channel] & ~filter) | int(shifted_data)
        # return modified pixel data
        return tuple(new_pixel)
    else:
        new_pixel = (old_pixel & ~filter) | int(shifted_data)
        # return modified pixel data
        return new_pixel


def text_to_binary(message):
    return ''.join([format(ord(char), '08b') for char in message])


def text_to_binary_to_text(binary_message):
    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])


def get_message_type(message):
    status = 0
    if len(message) > 4 and message[len(message)-4:] == '.txt':
        status = 2
    else:
        status = 1
    return status


# status -6 too many args
# status -5 too few args
# status -4 : -2 overloaded input
# status -1 undefined behavior flag given as image/message
# status 0 nothing happened
# status 1 all good, secret message is a string
# status 2 all good, secret message is a txt
def handle_argv(argv):
    status = 0
    force = False
    input_file = ""
    output_file = ""
    secret_message = ""
    unflagged_args = []
    current_flag = ""
    for arg in argv:
        # if there is a current flag & arg is a flag
        if current_flag != "" and arg[0:1] == '-':
            return [-1]
        match arg:
            # flags
            case '--string':
                current_flag = 'input string'
            case '-s':
                current_flag = 'input string'
            case '--text-file':
                current_flag = 'text file'
            case '-t':
                current_flag = 'text file'
            case '--input-image':
                current_flag = 'input image'
            case '-i':
                current_flag = 'input image'
            case '--output-image':
                current_flag = 'output image'
            case '-o':
                current_flag = 'output image'
            case '-f':
                force = True
            # input arg
            case _:
                if current_flag != "":
                    match current_flag:
                        case 'input string':
                            if secret_message != "":
                                return [-2]
                            else:
                                status = 1
                                secret_message = arg
                        case 'text file':
                            if secret_message != "":
                                return [-2] 
                            else:
                                status = 2
                                secret_message = arg
                        case 'input image':
                            if input_file != "":
                                return [-3]
                            else:
                                input_file = arg
                        case 'output image':
                            if output_file != "":
                                return [-4]
                            else:
                                output_file = arg
                    current_flag = ""
                else:
                    unflagged_args.append(arg)

    # handle unflagged args
    if secret_message == "":
        if len(unflagged_args) > 0:
            secret_message = unflagged_args[-1]
            unflagged_args = unflagged_args[:len(unflagged_args)-1]
            if secret_message[len(secret_message)-4:] == '.txt':
                status = 2
            else:
                status = 1
        else:
            return [-5]
    if input_file == "":
        if len(unflagged_args) > 0:
            input_file = unflagged_args[0]
            unflagged_args = unflagged_args[1:len(unflagged_args)]
        else:
            return [-5]
    if output_file == "":
        if len(unflagged_args) > 0:
            output_file = unflagged_args[0]
            unflagged_args = unflagged_args[1:len(unflagged_args)]
        else:
            output_file = "output" + '.' + input_file.split('.')[-1]

    if len(unflagged_args) == 0:
        return [status, input_file, output_file, secret_message, force]
    else:
        return [-6]


def main():
    standardized_argv = handle_argv(sys.argv[1:len(sys.argv)])
    status = standardized_argv[0]
    if status > 0:
        input_file = standardized_argv[1]
        output_file = standardized_argv[2]
        secret_message = standardized_argv[3]
        force = standardized_argv[4]

    match status:
        case -6:
            print("Error, Too Many Arguments")
        case -5:
            print("Error, Too Few Arguments")
        case -4:
            print("Error, Multiple Output Files Given")
        case -3:
            print("Error, Multiple Input Files Given")
        case -2:
            print("Error, Multiple Messages Given")
        case -1:
            print("Error, Flag Given as Input to Flag")
        case 1:
            file_errors = False
            if not os.path.isfile(input_file):
                print("Error, Input Image Does Not Exist")
                file_errors = True
            if os.path.isfile(output_file) and not force:
                print("Warning, Output Image Exists\nOverwrite? Specify -f")
                file_errors = True
            if not file_errors:
                bad_input = 1
                bad_output = 2
                extention_errors = 0
                try:
                    Image.open(input_file)
                except UnidentifiedImageError:
                    extention_errors += bad_input
                if os.path.isfile(output_file):
                    try:
                        Image.open(output_file)
                    except ValueError:
                        extention_errors += bad_output
                else:
                    try:
                        image = Image.new(mode='RGB', size=(1, 1))
                        image.save(output_file)
                    except ValueError:
                        extention_errors += bad_output
                if extention_errors == bad_input:
                    print("Error, Invalid Input Extention")
                    file_errors = True
                elif extention_errors == bad_output:
                    print("Error, Invalid Output Extention")
                    file_errors = True
                elif extention_errors == bad_input + bad_output:
                    print("Error, Invalid Input & Output Extention")
                    file_errors = True
            if not file_errors:
                binary_message = text_to_binary(secret_message)
                if modify_image_string(input_file, output_file, binary_message) != -1:
                    print(f"Success, String Embeded in Image: {output_file}")
                else:
                    print("Aborting, Image Cannot Contain Message Data")
        case 2:
            file_errors = False
            if not os.path.isfile(input_file):
                print("Error, Input Image Does Not Exist")
                file_errors = True
            if os.path.isfile(output_file) and not force:
                print("Warning, Output Image Exists\nOverwrite? Specify -f")
                file_errors = True
            if not os.path.isfile(secret_message):
                print("Error, Message File Does Not Exist")
                file_errors = True
            if not file_errors:
                bad_input = 1
                bad_output = 2
                extention_errors = 0
                try:
                    Image.open(input_file)
                except UnidentifiedImageError:
                    extention_errors += bad_input
                if os.path.isfile(output_file):
                    try:
                        Image.open(output_file)
                    except ValueError:
                        extention_errors += bad_output
                else:
                    try:
                        image = Image.new(mode='RGB', size=(1, 1))
                        image.save(output_file)
                        os.remove(output_file)
                    except ValueError:
                        extention_errors += bad_output
                if extention_errors == bad_input:
                    print("Error, Invalid Input Extention")
                    file_errors = True
                elif extention_errors == bad_output:
                    print("Error, Invalid Output Extention")
                    file_errors = True
                elif extention_errors == bad_input + bad_output:
                    print("Error, Invalid Input & Output Extention")
                    file_errors = True
            if not file_errors:
                if modify_image_txt(input_file, output_file, secret_message) != -1:
                    print(f"Success, TXT File Contents Embeded in Image: {output_file}")
                else:
                    print("Aborting, Image Cannot Contain Message Data")
        case _:
            print("Error, Unknown Error")


if __name__ == "__main__":
    main()
