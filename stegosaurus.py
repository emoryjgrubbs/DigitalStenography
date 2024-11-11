from subprocess import Popen, PIPE
import tkinter as tk
from tkinter import messagebox  # for print decode
from tkinter import filedialog  # for selecting files


def clear_text_feilds():
    input_img_entry.delete(0, 'end')
    output_img_entry.delete(0, 'end')
    input_txt_entry.delete(0, 'end')
    output_txt_entry.delete(0, 'end')


def handle_submit_click():
    if mode.get() == 'embed':
        input_img = input_img_entry.get()
        output_img = output_img_entry.get()
        input_txt = input_txt_entry.get()
        lsb_embed = Popen(['python', 'embed.py', input_img, output_img, input_txt, '-f'],
                          stdout=PIPE, stdin=PIPE, encoding='utf8')
        responce = lsb_embed.stdout.readline()
        # test_lbl = tk.Label(window, text=responce).pack()
    elif mode.get() == 'decode':
        input_img = input_img_entry.get()
        output_txt = output_txt_entry.get()
        lsb_decode = Popen(['python', 'decode.py', input_img, output_txt, '-f'],
                           stdout=PIPE, stdin=PIPE, encoding='utf8')
        responce = lsb_decode.stdout.readline()
        # test_lbl = tk.Label(window, text=responce).pack()


def clear_lsb_entry():
    list = frame_file_input.grid_slaves()
    for w in list:
        w.grid_forget()


def display_lsb_embed():
    mode.set('embed')
    clear_lsb_entry()
    # input image
    input_img_label.grid(row=1, column=1, sticky="w")
    input_img_entry.grid(row=2, column=1)
    input_img_entry.delete(0, 'end')
    input_img_btn.grid(row=2, column=2, padx=10)
    # output image
    output_img_label.grid(row=3, column=1, sticky="w")
    output_img_entry.grid(row=4, column=1)
    output_img_entry.delete(0, 'end')
    output_img_btn.grid(row=4, column=2)
    # input txt file
    input_txt_label.grid(row=5, column=1, sticky="w")
    input_txt_entry.grid(row=6, column=1)
    input_txt_entry.delete(0, 'end')
    input_txt_btn.grid(row=6, column=2)


def display_lsb_decode():
    mode.set('decode')
    clear_lsb_entry()
    # input image
    input_img_label.grid(row=1, column=1, sticky="w")
    input_img_entry.grid(row=2, column=1)
    input_img_entry.delete(0, 'end')
    input_img_btn.grid(row=2, column=2)
    # output txt file
    output_txt_label.grid(row=3, column=1, sticky="w")
    output_txt_entry.grid(row=4, column=1)
    output_txt_entry.delete(0, 'end')
    output_txt_btn.grid(row=4, column=2)


def open_img_file():
    title = "Select The Input Image"
    filetypes = (('Image Files', ('*.png', '*.jpg',
                                  '*.jpeg', '*.bmp',
                                  '*.gif', '*.tiff',
                                  '*.webp')),
                 ('All Files', '*'))
    path = filedialog.askopenfilename(initialdir="~/Downloads", title=title,
                                      filetypes=filetypes)
    input_img_entry.insert(0, path)


def save_img_file():
    title = "Select The Output Image"
    filetypes = (('Image Files', ('*.png', '*.jpg',
                                  '*.jpeg', '*.bmp',
                                  '*.gif', '*.tiff',
                                  '*.webp')),
                 ('All Files', '*'))
    path = filedialog.asksaveasfilename(initialdir="~/Downloads", title=title,
                                        filetypes=filetypes)
    output_img_entry.insert(0, path)


def open_txt_file():
    title = "Select The Text File to Embed"
    filetypes = (('Text Files', '*.txt'),
                 ('All Files', '*'))
    path = filedialog.askopenfilename(initialdir="~/Downloads", title=title,
                                      filetypes=filetypes)
    input_txt_entry.insert(0, path)


def save_txt_file():
    title = "Select The Location to Save The Decoded Data"
    filetypes = (('Text Files', '*.txt'),
                 ('All Files', '*'))
    path = filedialog.asksaveasfilename(initialdir="~/Downloads", title=title,
                                        filetypes=filetypes)
    output_txt_entry.insert(0, path)


# create stego program window
window = tk.Tk()
window.title("Stegosaurus")

# global variables that will be assigned & input to command
mode = tk.StringVar()
output_print = tk.BooleanVar()

# stegenography type title
lbl_mode = tk.Label(text="LSB Stegenography")
lbl_mode.pack(padx=10, pady=25)


# create embed/decode mode buttons
frame_mode = tk.Frame()
frame_mode.pack()

btn_lsb_embed = tk.Button(master=frame_mode, command=display_lsb_embed, text="Embed", width=15)
btn_lsb_embed.grid(row=0, column=0, padx=10, ipadx=10)

btn_lsb_decode = tk.Button(master=frame_mode, command=display_lsb_decode, text="Decode", width=15)
btn_lsb_decode.grid(row=0, column=1, padx=10, ipadx=10)


# create all types of input
frame_file_input = tk.Frame()
frame_file_input.pack()

# input feilds
# ------------
# input image
input_img_label = tk.Label(master=frame_file_input, text="Input Image")
input_img_entry = tk.Entry(master=frame_file_input, width=50)
input_img_btn = tk.Button(master=frame_file_input, command=open_img_file, text="Search")

# output image
output_img_label = tk.Label(master=frame_file_input, text="Output Image")
output_img_entry = tk.Entry(master=frame_file_input, width=50)
output_img_btn = tk.Button(master=frame_file_input, command=save_img_file, text="Search")

# input text file
input_txt_label = tk.Label(master=frame_file_input, text="Input Txt File")
input_txt_entry = tk.Entry(master=frame_file_input, width=50)
input_txt_btn = tk.Button(master=frame_file_input, command=open_txt_file, text="Search")

# input string
input_string_label = tk.Label(master=frame_file_input, text="Input String")
input_string_entry = tk.Entry(master=frame_file_input, width=50)

# output text file
output_txt_label = tk.Label(master=frame_file_input, text="Output Txt File")
output_txt_entry = tk.Entry(master=frame_file_input, width=50)
output_txt_btn = tk.Button(master=frame_file_input, command=save_txt_file, text="Search")


# Create a new frame `frame_buttons` to contain the
# Submit and Clear buttons. This frame fills the
frame_buttons = tk.Frame()
frame_buttons.pack(fill=tk.X, ipadx=5, ipady=5)

# Create the "Submit" button and pack it to the
btn_submit = tk.Button(master=frame_buttons, command=handle_submit_click, text="Submit")
btn_submit.pack(padx=10, ipadx=10)


# Start the application
display_lsb_embed()
window.mainloop()
