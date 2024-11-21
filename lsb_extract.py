from PIL import Image
import sys
import os


def extract_message_from_image(image_path, output_path):
    message_file = open(output_path, "wb")
    image = Image.open(image_path)
    pixels = image.load()

    width, height = image.size

    binary_message = ""
    end_of_message = '1111111111111110'

    # Loop through pixels
    for s in range(0, 8):
        for c in range(0, 2):
            for y in range(height):
                for x in range(width):
                    # TODO fix for greyscale
                    r, g, b = pixels[x, y]
                    filter = 2**s
                    match c:
                        # red
                        case 0:
                            binary_message += str((r & filter) >> s)
                        # green
                        case 1:
                            binary_message += str((g & filter) >> s)
                        # blue
                        case 2:
                            binary_message += str((b & filter) >> s)

                    # Check if the end of the message is reached
                    if len(binary_message) % 8 == 0 and binary_message.endswith(end_of_message):
                        # convert str to binary
                        message_file.write(str_bin_to_bytes(binary_message[:-len(end_of_message)]))
                        message_file.close()
                        return 1  # hidden message writen to file
                    elif len(binary_message) == 512:
                        # convert str to binary
                        message_file.write(str_bin_to_bytes(binary_message))
                        binary_message = ''

    message_file.close()
    return -1


def str_bin_to_bytes(str_str):
    if (len(str_str) % 8) != 0:
        # error should not be reachable
        return
    str_bytes = bytearray()  # empty byte string
    for i in range(0, len(str_str), 8):
        cur_int = 0
        for j in range(0, 8):
            if str_str[i+j] == '1':
                cur_int += 2 ** (7-j)
        cur_byte = cur_int.to_bytes(1)
        str_bytes.extend(cur_byte)
        # add the character in binay form to the end of bin
    return str_bytes


def print_txt(file_path):
    get_eof = open(file_path, "a")
    eof = get_eof.tell()
    get_eof.close()
    file = open(file_path, "r")
    
    file_index = 0

    while file_index + 512 < eof:
        message_chunk = file.read(512)
        print(message_chunk)
        file_index += 512
    message_chunk = file.read(eof - file_index)
    print(message_chunk)

    file.close()
    return 0


# status -6 too many args
# status -5 : -4 too few args
# status -3 : -2 overloaded input
# status -1 undefined behavior flag given as image/message
# status 0 nothing happened
# status 1 all good, secret message should be writen to specified file
# status 2 all good, secret message should be printed
def handle_argv(argv):
    status = 0
    force = False
    input_file = ""
    output_file = ""
    unflagged_args = []
    current_flag = ""
    for arg in argv:
        # if there is a current flag & arg is a flag
        if current_flag != "" and arg[0:1] == '-':
            return [-1]
        match arg:
            # flags
            case '--input':
                current_flag = 'input image'
            case '-i':
                current_flag = 'input image'
            case '--output':
                current_flag = 'output file'
            case '-o':
                current_flag = 'output file'
            case '--print':
                status = 2
                output_file = 'temp.txt'
            case '-p':
                status = 2
                output_file = 'temp.txt'
            case '-f':
                force = True
            # input arg
            case _:
                if current_flag != "":
                    match current_flag:
                        case 'input image':
                            if input_file != "":
                                return [-2]
                            else:
                                input_file = arg
                        case 'output file':
                            if output_file != "":
                                return [-3]
                            else:
                                output_file = arg
                    current_flag = ""
                else:
                    unflagged_args.append(arg)

    # handle unflagged args
    if input_file == "":
        if len(unflagged_args) > 0:
            input_file = unflagged_args[0]
            unflagged_args = unflagged_args[1:len(unflagged_args)]
        else:
            return [-4]
    if output_file == "":
        if len(unflagged_args) > 0:
            status = 1
            output_file = unflagged_args[0]
            unflagged_args = unflagged_args[1:len(unflagged_args)]
        else:
            return [-5]

    if len(unflagged_args) == 0:
        return [status, input_file, output_file, force]
    else:
        return [-6]


def main():
    standardized_argv = handle_argv(sys.argv[1:len(sys.argv)])
    status = standardized_argv[0]
    if status > 0:
        input_file = standardized_argv[1]
        output_file = standardized_argv[2]
        force = standardized_argv[3]

    match status:
        case -6:
            print("Error, Too Many Arguments Provided")
        case -5:
            print("Error, No Output File Provided")
        case -4:
            print("Error, No Input File Provided")
        case -3:
            print("Error, Multiple Output Files Provided")
        case -2:
            print("Error, Multiple Input Files Provided")
        case -1:
            print("Error, Flag Given as Input to Flag")
        case 1:
            file_errors = False
            if not os.path.isfile(input_file):
                print("Error, Input File Does Not Exist")
                file_errors = True
            if os.path.isfile(output_file) and not force:
                print("Warning, Output File Exists\nOverwrite? Specify -f")
                file_errors = True
            if not file_errors:
                message = extract_message_from_image(input_file, output_file)
                if message == 1:
                    print("Success, Message writen to file: ", output_file)
                else:
                    print("Warning, No Message Discovered")
                    os.remove(output_file)
        case 2:
            if not os.path.isfile(input_file):
                print("Error, Input File Does Not Exist")
            else:
                message = extract_message_from_image(input_file, output_file)
                if message == 1:
                    print_txt('temp.txt')
                    os.remove('temp.txt')
                else:
                    print("Warning, No Message Discovered")
                    os.remove('temp.txt')
        case _:
            print("Error, Unknown Error")



if __name__ == "__main__":
    main()
