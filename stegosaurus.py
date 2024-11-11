import tkinter as tk
from tkinter import messagebox  # for print decode
from tkinter import filedialog  # for selecting files


def handle_submit_click():
    global input_image
    global output_image
    global input_txt
    input_image = input_img_entry.get()
    output_image = output_img_entry.get()
    input_txt = input_txt_entry.get()
    command = get_command()
    lbl_test["text"] = command


def clear_lsb_entry():
    list = frame_file_input.grid_slaves()
    for w in list:
        w.grid_forget()


def display_lsb_embed():
    clear_lsb_entry()
    # input image
    input_img_label.grid(row=1, sticky="w")
    input_img_entry.grid(row=2)
    # output image
    output_img_label.grid(row=3, sticky="w")
    output_img_entry.grid(row=4)
    # input txt file
    input_txt_label.grid(row=5, sticky="w")
    input_txt_entry.grid(row=6)


def display_lsb_decode():
    clear_lsb_entry()
    # input image
    input_img_label.grid(row=1, sticky="w")
    input_img_entry.grid(row=2)
    # output txt file
    output_txt_label.grid(row=5, sticky="w")
    output_txt_entry.grid(row=6)


# create stego program window
window = tk.Tk()
window.title("Stegosaurus")

# global variables that will be assigned & input to command
input_image = ""
output_image = ""
input_txt = ""
output_txt = ""
output_print = tk.BooleanVar()
force = tk.BooleanVar()

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

# output image
output_img_label = tk.Label(master=frame_file_input, text="Output Image")
output_img_entry = tk.Entry(master=frame_file_input, width=50)

# input text file
input_txt_label = tk.Label(master=frame_file_input, text="Input Txt File")
input_txt_entry = tk.Entry(master=frame_file_input, width=50)

# input string
input_string_label = tk.Label(master=frame_file_input, text="Input String")
input_string_entry = tk.Entry(master=frame_file_input, width=50)

# input text file
output_txt_label = tk.Label(master=frame_file_input, text="Output Txt File")
output_txt_entry = tk.Entry(master=frame_file_input, width=50)


# Create a new frame `frame_buttons` to contain the
# Submit and Clear buttons. This frame fills the
frame_buttons = tk.Frame()
frame_buttons.pack(fill=tk.X, ipadx=5, ipady=5)

btn_force = tk.Checkbutton(master=frame_buttons, text="Force ", variable=force,
                           onvalue=True, offvalue=False, width=1, height=1)
btn_force.pack(padx=15, ipadx=10)

# Create the "Submit" button and pack it to the
btn_submit = tk.Button(master=frame_buttons, command=handle_submit_click, text="Submit")
btn_submit.pack(padx=10, ipadx=10)


# TODO testing
def get_command():
    return input_image + ", " + output_image + ", " + input_txt + ", force: " + str(force.get())


command = get_command()
lbl_test = tk.Label(text=command)
lbl_test.pack()

# Start the application
display_lsb_embed()
window.mainloop()
