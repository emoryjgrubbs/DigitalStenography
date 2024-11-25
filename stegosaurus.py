from subprocess import Popen, PIPE
import sys
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

        # icons
        pixmapi = getattr(qtw.QStyle.StandardPixmap, "SP_DirIcon")
        browse_icon = self.style().standardIcon(pixmapi)

        # method title
        method_lbl = qtw.QLabel("Least Significant Bit - Stegenography")
        method_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        method_lbl.setFont(qtg.QFont('Helvetica', 16))

        # mode tab
        mode_tab = qtw.QTabWidget()

        # hide mode page
        hide_pge = qtw.QWidget(mode_tab)
        hide_pge.setLayout(qtw.QFormLayout())
        hide_pge.layout().setHorizontalSpacing(25)
        mode_tab.addTab(hide_pge, "Hide Message")
        # hide message inputs
        hide_cover_lbl = qtw.QLabel("Cover Image:")
        hide_pge.layout().addRow(hide_cover_lbl)
        hide_cover_ent = qtw.QLineEdit()
        hide_cover_ent.setPlaceholderText("Enter the path to the cover image")
        hide_cover_dialog = hide_cover_ent.addAction(browse_icon, hide_cover_ent.ActionPosition(1))
        hide_cover_dialog.triggered.connect(lambda: get_path("hide_cover"))
        hide_pge.layout().addRow(hide_cover_ent)

        hide_stego_lbl = qtw.QLabel("Stego Image:")
        hide_pge.layout().addRow(hide_stego_lbl)
        hide_stego_ent = qtw.QLineEdit()
        hide_stego_ent.setPlaceholderText("Enter location to save the stego image")
        hide_stego_dialog = hide_stego_ent.addAction(browse_icon, hide_stego_ent.ActionPosition(1))
        hide_stego_dialog.triggered.connect(lambda: get_path("hide_stego"))
        hide_pge.layout().addRow(hide_stego_ent)

        hide_msg_lbl = qtw.QLabel("Message File:")
        hide_msg_chk = qtw.QCheckBox("Hide String?", clicked=lambda: switch_hide_ent())
        hide_pge.layout().addRow(hide_msg_lbl, hide_msg_chk)
        hide_txt_ent = qtw.QLineEdit()
        hide_txt_ent.setPlaceholderText("Enter the path to the message text file")
        hide_txt_dialog = hide_txt_ent.addAction(browse_icon, hide_txt_ent.ActionPosition(1))
        hide_txt_dialog.triggered.connect(lambda: get_path("hide_txt"))
        hide_pge.layout().addRow(hide_txt_ent)
        hide_str_ent = qtw.QTextEdit()
        hide_str_ent.setPlaceholderText("Enter the message to hide")
        hide_pge.layout().addRow(hide_str_ent)
        hide_pge.layout().setRowVisible(hide_str_ent, False)

        # hide message submit
        hide_btn = qtw.QPushButton("Submit", clicked=lambda: handle_submit("hide_file"))
        hide_pge.layout().addRow(hide_btn)

        # extract mode page
        extract_pge = qtw.QWidget(mode_tab)
        extract_pge.setLayout(qtw.QFormLayout())
        extract_pge.layout().setHorizontalSpacing(25)
        mode_tab.addTab(extract_pge, "Extract Message")
        # extract message inputs
        extract_stego_lbl = qtw.QLabel("Stego Image:")
        extract_pge.layout().addRow(extract_stego_lbl)
        extract_stego_ent = qtw.QLineEdit()
        extract_stego_ent.setPlaceholderText("Enter the path to the stego image")
        extract_stego_dialog = extract_stego_ent.addAction(browse_icon, extract_stego_ent.ActionPosition(1))
        extract_stego_dialog.triggered.connect(lambda: get_path("extract_stego"))
        extract_pge.layout().addRow(extract_stego_ent)

        extract_txt_lbl = qtw.QLabel("Data File:")
        extract_out_chk = qtw.QCheckBox("Print Message?", clicked=lambda: switch_extract_out())
        extract_pge.layout().addRow(extract_txt_lbl, extract_out_chk)
        extract_txt_ent = qtw.QLineEdit()
        extract_txt_ent.setPlaceholderText("Enter the location to save the message")
        extract_txt_dialog = extract_txt_ent.addAction(browse_icon, extract_txt_ent.ActionPosition(1))
        extract_txt_dialog.triggered.connect(lambda: get_path("extract_txt"))
        extract_pge.layout().addRow(extract_txt_ent)
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


        def switch_hide_ent():
            if hide_msg_chk.checkState() == Qt.CheckState.Checked:
                hide_pge.layout().setRowVisible(hide_txt_ent, False)
                hide_pge.layout().setRowVisible(hide_str_ent, True)
                hide_msg_lbl.setText("Message String:")
            else:
                hide_pge.layout().setRowVisible(hide_str_ent, False)
                hide_pge.layout().setRowVisible(hide_txt_ent, True)
                hide_msg_lbl.setText("Message File:")


        def switch_extract_out():
            if extract_out_chk.checkState() == Qt.CheckState.Checked:
                extract_txt_ent.setDisabled(True)
                extract_txt_dialog.setDisabled(True)
            else:
                extract_txt_ent.setEnabled(True)
                extract_txt_dialog.setEnabled(True)


        def handle_submit(mode):
            stego_folder_path = sys.argv[0]
            # path - 'stegosaurus.py'
            stego_folder_path = stego_folder_path[0:len(stego_folder_path)-14]
            match mode:
                case 'hide_file':
                    input_img = hide_cover_ent.text()
                    output_img = hide_stego_ent.text()
                    input_txt = hide_txt_ent.text()
                    input_str = hide_str_ent.toPlainText()
                    if hide_msg_chk.checkState() == Qt.CheckState.Checked:
                        lsb_embed = Popen(['python', stego_folder_path + 'lsb_hide.py', input_img, output_img, '-s', input_str, '-f'],
                                          stdout=PIPE, encoding='utf8')
                    else:
                        lsb_embed = Popen(['python', stego_folder_path + 'lsb_hide.py', input_img, output_img, '-t', input_txt, '-f'],
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
                    hide_str_ent.setText("")
                case 'extract':
                    input_img = extract_stego_ent.text()
                    output_txt = extract_txt_ent.text()
                    if extract_out_chk.checkState() == Qt.CheckState.Checked:
                        lsb_decode = Popen(['python', stego_folder_path + 'lsb_extract.py', input_img, '-p', '-f'],
                                           stdout=PIPE, encoding='utf8')
                    else:
                        lsb_decode = Popen(['python', stego_folder_path + 'lsb_extract.py', input_img, output_txt, '-f'],
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
                            pop_up.setIcon(qtw.QMessageBox.Icon.Information)
                            pop_up.setText("The Message is: ")
                            pop_up.setText(responce)
                            pop_up.exec()
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

