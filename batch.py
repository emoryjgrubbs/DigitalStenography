from subprocess import Popen, PIPE
import os

for (root,dirs,files) in os.walk('/home/Emu/Downloads/txt-files/', topdown=True):
    x = 1
sorted_files = files.sort()

images = ['skip', 'skip', 'Maltese.bmp']
methods = ['normal.py', 'invert.py', 'color.py', 'msb.py']

def main():
    global sorted_files
    global images
    global methods

    # X,Y,Color_Channel,Modify_Bit,PSNR,MSE,SPACE,SPACE
    csv_string = ""

    steps_complete = 0

    print_progress(steps_complete)
    for file in files:
        csv_string += file + ','
        for image in images:
            if image == 'skip':
                empty_record = ',,,,,,,,' 
                for method in methods:
                    csv_string += empty_record

                    steps_complete += 1
                    print_progress(steps_complete)

            else:
                for method in methods:
                    path = '/home/Emu/Downloads/txt-files/' + file
                    hide = Popen(['python', method, image, 'output.bmp', '-t', path, '-f'],
                                 stdout=PIPE, encoding='utf8')
                    responce = hide.stdout.readline()

                    if responce.strip(' \t\n\r') != 'abort':
                        while responce != '':
                            csv_string += responce.strip(' \t\n\r')
                            csv_string += ','
                            responce = hide.stdout.readline()

                        analyse = Popen(['python', 'psnr.py', image, 'output.bmp'],
                                        stdout=PIPE, encoding='utf8')
                        psnr = analyse.stdout.readline().strip(' \t\n\r')
                        mse = analyse.stdout.readline().strip(' \t\n\r')
                        csv_string += psnr + ',' + mse + ','
                        steps_complete += 1
                        print_progress(steps_complete)
                    else:
                        empty_fields = ',,,,,,' 
                        csv_string += empty_fields
                        steps_complete += 1
                        print_progress(steps_complete)

                    spacer = ',,'
                    csv_string += spacer

        csv_string += '\n'

    data_file = open('data.csv', mode='a', newline=None)
    data_file.write(csv_string)
    data_file.close()


def print_progress(steps_complete):
    progress = '['

    total_progress = len(files) * len(images) * len(methods)
    for i in range(0, total_progress):
        if steps_complete >= i:
            progress += '#'
        else:
            progress += ' '

    progress += ']'
    print(progress, end="\r", flush=True)


main()
