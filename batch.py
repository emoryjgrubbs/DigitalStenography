from subprocess import Popen, PIPE
import os

for (root,dirs,files) in os.walk('/home/Emu/Downloads/txt-files/', topdown=True):
    x = 1

images = ['cablecar.bmp', 'Rainer.bmp', 'Maltese.bmp']
methods = ['normal.py', 'invert.py', 'color.py', 'msb.py']

# X,Y,Color_Channel,Modify_Bit,PSNR,MSE,SPACE,SPACE
csv_string = ""
for file in files:
    for image in images:
        for method in methods:
            path = '/home/Emu/Downloads/txt-files/' + file
            hide = Popen(['python', method, image, 'output.bmp', '-t', path, '-f'],
                         stdout=PIPE, encoding='utf8')
            responce = hide.stdout.readline()

            if responce.split(',')[0] != 'Aborting':
                while responce != '':
                    csv_string += responce.strip(' \t\n\r')
                    csv_string += ','
                    responce = hide.stdout.readline()

                analyse = Popen(['python', 'psnr.py', image, 'output.bmp'],
                                stdout=PIPE, encoding='utf8')
                psnr = analyse.stdout.readline().strip(' \t\n\r')
                mse = analyse.stdout.readline().strip(' \t\n\r')
                csv_string += psnr + ',' + mse + ','
            else:
                empty_fields = ',,,,,,' 
                csv_string += empty_fields

            spacer = ',,'
            csv_string += spacer

    csv_string += '\n'

print(csv_string)

