from subprocess import Popen, PIPE
import os
from PyQt6.QtCore import Qt
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg


class Stegosaurus(qtw.QWidget):
    def __init__(self):
        super().__init__()
        # title
        self.setWindowTitle("Stegosaurus")

        # layout
        self.setLayout(qtw.QVBoxLayout())

        # method title
        method_lbl = qtw.QLabel("Least Significant Bit - Stegenography")
        method_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        method_lbl.setFont(qtg.QFont('Helvetica', 16))

        # mode tab
        mode_tab = qtw.QTabWidget()

        # hide mode page
        hide_pge = qtw.QWidget(mode_tab)
        hide_pge.setLayout(qtw.QFormLayout())
        mode_tab.addTab(hide_pge, "Hide Message")
        # hide message inputs
        hide_cover_ent = qtw.QLineEdit()
        hide_cover_ent.setPlaceholderText("Enter the path to the cover image")
        hide_cover_dialog = qtw.QPushButton("Browse", clicked=lambda: get_path("hide_cover"))
        hide_pge.layout().addRow(hide_cover_ent, hide_cover_dialog)
        hide_stego_ent = qtw.QLineEdit()
        hide_stego_ent.setPlaceholderText("Enter location to save the stego image")
        hide_stego_dialog = qtw.QPushButton("Browse", clicked=lambda: get_path("hide_stego"))
        hide_pge.layout().addRow(hide_stego_ent, hide_stego_dialog)
        hide_txt_ent = qtw.QLineEdit()
        hide_txt_ent.setPlaceholderText("Enter the path to the message text file")
        hide_txt_dialog = qtw.QPushButton("Browse", clicked=lambda: get_path("hide_txt"))
        hide_pge.layout().addRow(hide_txt_ent, hide_txt_dialog)
        hide_str_ent = qtw.QTextEdit()
        hide_str_ent.setPlaceholderText("Enter the message to hide")
        # hide message submit
        hide_btn = qtw.QPushButton("Submit", clicked=lambda: handle_submit("hide_file"))
        hide_pge.layout().addRow(hide_btn)

        # extract mode page
        extract_pge = qtw.QWidget(mode_tab)
        extract_pge.setLayout(qtw.QFormLayout())
        mode_tab.addTab(extract_pge, "Extract Message")
        # extract message inputs
        extract_stego_ent = qtw.QLineEdit()
        extract_stego_ent.setPlaceholderText("Enter the path to the stego image")
        extract_stego_dialog = qtw.QPushButton("Browse", clicked=lambda: get_path("extract_stego"))
        extract_pge.layout().addRow(extract_stego_ent, extract_stego_dialog)
        extract_txt_ent = qtw.QLineEdit()
        extract_txt_ent.setPlaceholderText("Enter the location to save the message")
        extract_txt_dialog = qtw.QPushButton("Browse", clicked=lambda: get_path("extract_txt"))
        extract_pge.layout().addRow(extract_txt_ent, extract_txt_dialog)
        # hide message submit
        extract_btn = qtw.QPushButton("Submit", clicked=lambda: handle_submit("extract"))
        extract_pge.layout().addRow(extract_btn)

        # display
        self.layout().addWidget(method_lbl)
        self.layout().addWidget(mode_tab)
        self.show()

        def get_path(entry):
            # TODO works on linux not sure about windows
            start_dir = os.path.expanduser('~') + '/Downloads'
            img_file_types = "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp);;All Files (*)"
            txt_file_types = "Image Files (*.txt);;All Files (*)"
            match entry:
                case 'hide_cover':
                    path = qtw.QFileDialog.getOpenFileName(self, "Select The Cover Image to Hide The Data", start_dir, img_file_types)
                    if path:
                        hide_cover_ent.setText(path[0])
                case 'hide_stego':
                    path = qtw.QFileDialog.getSaveFileName(self, "Select The Location to save The Stego Image", start_dir, img_file_types)
                    if path:
                        hide_stego_ent.setText(path[0])
                case 'hide_txt':
                    path = qtw.QFileDialog.getOpenFileName(self, "Select The Message Text File", start_dir, txt_file_types)
                    if path:
                        hide_txt_ent.setText(path[0])
                case 'extract_stego':
                    path = qtw.QFileDialog.getOpenFileName(self, "Select The Stego Image to Extract", start_dir, img_file_types)
                    if path:
                        extract_stego_ent.setText(path[0])
                case 'extract_txt':
                    path = qtw.QFileDialog.getSaveFileName(self, "Select Location to Save The Message", start_dir, txt_file_types)
                    if path:
                        extract_txt_ent.setText(path[0])



        def handle_submit(mode):
            match mode:
                case 'hide_file':
                    input_img = hide_cover_ent.text()
                    output_img = hide_stego_ent.text()
                    input_txt = hide_txt_ent.text()
                    lsb_embed = Popen(['python', 'lsb_hide.py', input_img, output_img, '-t', input_txt, '-f'],
                                      stdout=PIPE, encoding='utf8')
                    responce = lsb_embed.stdout.readline()
                    match responce.split(',')[0]:
                        case 'Success':
                            pop_up = qtw.QMessageBox()
                            pop_up.setWindowTitle("Stegosaurus Success")
                            pop_up.setIcon(qtw.QMessageBox.Icon.Information)
                            pop_up.setText(responce)
                            pop_up.exec()
                        case 'Error':
                            pop_up = qtw.QMessageBox()
                            pop_up.setWindowTitle("Stegosaurus Error")
                            pop_up.setIcon(qtw.QMessageBox.Icon.Critical)
                            pop_up.setText(responce)
                            pop_up.exec()
                        case 'Aborting':
                            pop_up = qtw.QMessageBox()
                            pop_up.setWindowTitle("Stegosaurus Error")
                            pop_up.setIcon(qtw.QMessageBox.Icon.Warning)
                            pop_up.setText(responce)
                            pop_up.exec()
                    hide_cover_ent.setText("")
                    hide_stego_ent.setText("")
                    hide_txt_ent.setText("")
                case 'extract':
                    input_img = extract_stego_ent.text()
                    output_txt = extract_txt_ent.text()
                    lsb_decode = Popen(['python', 'lsb_extract.py', input_img, output_txt, '-f'],
                                       stdout=PIPE, encoding='utf8')
                    responce = lsb_decode.stdout.readline()
                    match responce.split(',')[0]:
                        case 'Success':
                            pop_up = qtw.QMessageBox()
                            pop_up.setWindowTitle("Stegosaurus Success")
                            pop_up.setIcon(qtw.QMessageBox.Icon.Information)
                            pop_up.setText(responce)
                            pop_up.exec()
                        case 'Error':
                            pop_up = qtw.QMessageBox()
                            pop_up.setWindowTitle("Stegosaurus Error")
                            pop_up.setIcon(qtw.QMessageBox.Icon.Critical)
                            pop_up.setText(responce)
                            pop_up.exec()
                        case _:
                            # TODO
                            pop_up = qtw.QMessageBox()
                            pop_up.setWindowTitle("Stegosaurus Success")
                            # should just be for when message is printed
                            # new window to display output
                            # while responce:
                            #     output_lbl 
                            #     responce = lsb_decode.stdout.readline()
                    extract_stego_ent.setText("")
                    extract_txt_ent.setText("")


app = qtw.QApplication([])
window = Stegosaurus()
app.exec()

