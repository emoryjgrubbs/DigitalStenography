# Image Pixel Modifier

This Python script allows you to access and modify pixel values of an image while keeping the image header intact. It uses the `Pillow` library to manipulate images, for both hiding and extracting the data.

## Prerequisites

Make sure you have Python installed on your system. You also need the `Pillow` and `PyQt6` library to run this script.

## Installation

1. Clone this repository or download the files.
2. Install the required Python packages by running:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### GUI

1. Run the Python gui program

    ```bash
    python stegosaurus.py
    ```

2. Interact with the program to hide or extract data

### Command Line

1. Run the Python program to encode the message

    ```bash
    python lsb_hide.py [input image] [output image] [message]
    ```
    
    input image: the cover image to be modified
   
    output image: the modified stego image (if unspecified, default to output.png)
   
    message: the text to be hidden (either simple string text or the path to a file ending in .txt)

    flags can be used as an alternative format, they can appear in any order, and any unflagged input will be matched in the standard order to the needed input

```
    --input-image [input image]
        -i [input image]
    --output-image [output image]
        -o [output image]
    --string [message]
        -s [message]
    --text-file [message]
        -t [message]

    -f: overwrite the image specified by the [output image]
```

3. Run the Python program to decode the message
    
    ```bash
    python lsb_extract.py [input image] [output file]
    ```

    input image: the stego image to decode
   
    output file: the extracted message data

    flags can be used as an alternative format, they can appear in any order, and any unflagged input will be matched in the standard order to the needed input

```
    --input [input image]
        -i [input image]
    --output [output file]
        -o [output file]
   
    --print: print the data as text to standard out instead of [output file] (temp.txt will be created then destroyed)
        -p: print the data...
    -f: overwrite the image specified by the [output file]
```

5. Run the Python program to check the level of modification to the image

    ```bash
    python psnr.py [cover image] [stego image]
    ```


## Files

- `stegosaurus.py`: Program to hide/extract data graphically
- `lsb_hide.py`: Program to hide data in a cover image
- `lsb_extract.py`: Program to extract data from a stego image
- `requirements.txt`: Lists the required Python packages (`Pillow`, `PyQt`).
- `README.md`: This file.
