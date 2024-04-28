import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import PyQt6.QtSvgWidgets as qtsvg
import PyQt6.QtWidgets as qtw
# from utils.scanner.auto_warp import Scanner
import os
import sys
from decimal import Decimal

if __name__ == '__main__':
    # from scanner.manual_warp import ManualImageWarper
    from teste import *
else:
    from utils.scanner.manual_warp import ManualImageWarper


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PYQT GUI")
        self.setStyleSheet("background-color: #1A1E23;")
        self.setMinimumSize(640, 480)
        self.count = 0
        self.selected_files = []
        self.selected_folder = []
        self.save_at_path = ""
        self.initUI()
        self.resize(640, 480)
        self.img = []



    def initUI(self):
        # Create Main Window layout

        main_layout = qtw.QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create Left Frame Parent
        self.left_frame_stacker = qtw.QStackedWidget(self)
        self.left_frame_stacker.setMinimumSize(int(self.width()*0.6), self.height())
        print(self.left_frame_stacker.size())
        # self.left_frame_stacker.setMaximumWidth(int(self.width() * 0.6))
        self.left_frame_stacker.setStyleSheet("background-color: black;")
        

        # Create Left Frame("Main" frame)
        self.left_frame_init = qtw.QWidget(self.left_frame_stacker)
        self.left_frame_init.setMinimumHeight(self.height())
        # self.left_frame_init.setFixedWidth(self.left_frame_stacker.width())
        self.left_frame_init.setStyleSheet("background-color: #1A1E23 ;")


        # Create Alternative Left Frame
        self.left_frame_alt = qtw.QWidget(self.left_frame_stacker)
        self.left_frame_alt.setMinimumHeight(self.height())
        # self.left_frame_alt.setFixedWidth(self.left_frame_stacker.width())
        self.left_frame_alt.setStyleSheet("background-color: blue;")

        self.left_frame_list = qtw.QListWidget(self.left_frame_stacker)
        self.left_frame_list.setAlternatingRowColors(True)
        self.left_frame_list.setIconSize(qtc.QSize(128, 128))


        self.left_frame_list.setStyleSheet('''                                                QListWidget {
                                                background: #1A1E23; 
                                                border: none; 
                                                color: white;
                                                
                                                }

                                                QListWidget::item{
                                                margin-left: 16px;
                                                alternate-background-color: #23282F;
                                                  }

                                                  ''')

        self.left_frame_list.setMinimumHeight(self.height())
        self.left_frame_list.setMinimumSize(int(self.width()*0.6), self.height())

        self.left_frame_list.setSizePolicy(qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Expanding)
        self.left_frame_list.setFont(qtg.QFont("Poppins Medium"))

        self.lf_img_display_layout = qtw.QVBoxLayout()
  

        self.lf_img_display_layout.addWidget(self.left_frame_list)


            # pixmap = qtg.QPixmap("assets/img/logo.png")
            # logo_img.setPixmap(pixmap)
            # logo_img.resize(pixmap.width(), pixmap.height())
            # logo_img.setMaximumHeight(logo_img.height() + 2)
            # logo_img.setStyleSheet("padding-bottom:2px")
            
            
        # Create Right Frame
        self.right_frame = qtw.QWidget(self)
        self.right_frame.setMinimumHeight(self.height())
        # self.right_frame.setMinimumWidth(300)
        self.right_frame.setStyleSheet("background-color: #2B323B;")

        # Create Left Frame Layout
        self.left_frame_init_layout = qtw.QVBoxLayout(self.left_frame_init)
        self.left_frame_init_layout.setContentsMargins(36, 36, 36, 36)
        self.left_frame_init_layout.setSpacing(0)

        # Create Left Frame alternative layout
        self.left_frame_alt_layout = qtw.QVBoxLayout(self.left_frame_alt)
        self.left_frame_alt_layout.setContentsMargins(0, 0, 0, 0)
        self.left_frame_alt_layout.setSpacing(0)
        self.left_frame_alt_layout.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)


        # Create Right Frame Layout
        self.right_frame_layout = qtw.QVBoxLayout(self.right_frame)
        self.right_frame_layout.setContentsMargins(32, 140, 32, 110)  # Set margins to add some padding
        self.right_frame_layout.setAlignment(qtc.Qt.AlignmentFlag.AlignTop)
        self.right_frame_layout.setSpacing(0)

        #Create Logo
        logo_img = qtw.QLabel()
        pixmap = qtg.QPixmap("assets/img/logo.png")
        logo_img.setPixmap(pixmap)
        logo_img.resize(pixmap.width(), pixmap.height())
        logo_img.setMaximumHeight(logo_img.height() + 2)
        logo_img.setStyleSheet("padding-bottom:2px")

        #Create Logo Subtitle
        logo_subtitle = qtw.QLabel("Escaneie seus documentos:", self.left_frame_init)
        logo_subtitle.setStyleSheet("color: #B24417; font-size: 11pt")
        logo_subtitle.setFont(qtg.QFont("Poppins Medium"))
        logo_subtitle.setMaximumHeight(logo_subtitle.height())

        # Create Drag'n Drop Rectangle

        self.drag_n_drop_container = qtw.QWidget()
        self.drag_n_drop_container.setSizePolicy(qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Expanding)
        
        self.dnd_container_layout = qtw.QHBoxLayout()
        self.dnd_container_layout.setSpacing(0)
        self.dnd_container_layout.setContentsMargins(0, 0, 0, 0)

        self.drag_n_drop_container.setLayout(self.dnd_container_layout)

     
        self.drag_n_drop_rectangle = qtw.QWidget()
        self.drag_n_drop_rectangle.setStyleSheet("background-color:#192B32; border-radius:8px; border: 2px dashed #17C4EC ")
        self.drag_n_drop_rectangle.setAcceptDrops(True)
        self.drag_n_drop_rectangle.setObjectName("drag_n_drop_rectangle")

        self.drag_n_drop_rectangle.setSizePolicy(qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Expanding)


        self.drag_n_drop_rectangle.dragEnterEvent = self.dragEnterEvent
        self.drag_n_drop_rectangle.dropEvent = self.dropEvent

        # parent = self.left_frame_dnd_layout
        # children = parent.children()
        # for child in children:
        #     print(child.objectName())
        #     # print(type(child).__name__)

        # Create Drag'n Drop Inner Layout
        drag_n_drop_inner_layout = qtw.QVBoxLayout(self.drag_n_drop_rectangle)
        drag_n_drop_inner_layout.setSpacing(0)
        drag_n_drop_inner_layout.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        # Create Drag'n Drop "Drop here" Text
        drag_n_drop_label_txt = qtw.QLabel("Arraste e solte arquivos aqui ou", self.drag_n_drop_rectangle)
        drag_n_drop_label_txt.setFixedHeight(drag_n_drop_label_txt.height()-10)
        drag_n_drop_label_txt.setStyleSheet("font-size: 16px; padding-right:1px; color: #17C4EC; border: none; letter-spacing: -0.3px; border-radius:0")
        drag_n_drop_label_txt.setFont(qtg.QFont("Poppins Medium"))
        drag_n_drop_label_txt.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)

        # Create Drag'n Drop "Choose from files" Hypertext
        drag_n_drop_hypertxt = qtw.QLabel("ESCOLHER DOS ARQUIVOS", self.drag_n_drop_rectangle)
        drag_n_drop_hypertxt.setStyleSheet("font-size: 19px; font-weight:bold; color: #17C4EC; border: none; letter-spacing: -0.1px; text-decoration: underline; border-radius: 0")
        drag_n_drop_hypertxt.setFixedHeight(drag_n_drop_hypertxt.sizeHint().height()-8)
        drag_n_drop_hypertxt.setFont(qtg.QFont("Poppins"))
        drag_n_drop_hypertxt.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        drag_n_drop_hypertxt.mousePressEvent = self.openFileDialog
        drag_n_drop_hypertxt.enterEvent = self.changeCursorToHand
        drag_n_drop_hypertxt.leaveEvent = self.changeCursorToArrow

        #Create SVG Folder Icon
        upload_files_folder_icon = qtsvg.QSvgWidget("assets/img/upload-files.svg", self.drag_n_drop_rectangle)
        upload_files_folder_icon.setMinimumSize(qtc.QSize(100, 100))  # Set the minimum size
        upload_files_folder_icon.setFixedSize(40, 40)
        upload_files_folder_icon.setStyleSheet("border: none")

        # Create image display || Left frame variation




        ###RIGHT FRAME
        ## INPUT LABEl
        # Create label for "Selected Images" input
        self.select_img_input_btn_label = qtw.QLabel("Selecionar:")
        self.select_img_input_btn_label.setStyleSheet("color:white; font-size:10.5pt")
        self.select_img_input_btn_label.setFont(qtg.QFont("Poppins Medium"))
        self.select_img_input_btn_label.setAlignment(qtc.Qt.AlignmentFlag.AlignTop)
        self.select_img_input_btn_label.setFixedHeight(self.select_img_input_btn_label.sizeHint().height()+4) #setting a padding of 4

        # Create label for "Save at" input
        self.save_at_input_label = qtw.QLabel("Salvar em:")
        self.save_at_input_label.setStyleSheet("color:white; font-size:10.5pt")
        self.save_at_input_label.setFont(qtg.QFont("Poppins Medium"))
        self.save_at_input_label.setAlignment(qtc.Qt.AlignmentFlag.AlignTop)
        self.save_at_input_label.setFixedHeight(self.save_at_input_label.sizeHint().height()+4) #setting a padding of 4



        ## INPUT
        # Create "Selected images" Dropdown
   
        # Create "Save at" Input
        self.save_at_input = qtw.QLineEdit()
        self.save_at_input.setPlaceholderText("Exemplo: C:/caminho/img.png")
        self.save_at_input.setStyleSheet("background-color: #1A1E23; color: white; border: 0; height: 27px; padding-left: 6px; padding-bottom: 1px; font-size: 9pt; border-radius: 4px;")
        self.save_at_input.setFont(qtg.QFont("Poppins"))
        self.save_at_input.mousePressEvent = lambda event: self.verifyInputValue("save_at_input")
    
        self.btn_container = qtw.QHBoxLayout()
        self.select_img_input_btn = qtw.QPushButton("File")
        self.select_img_input_btn.setFont(qtg.QFont("Poppins"))
        self.select_img_input_btn.setFixedWidth(self.save_at_input.widthMM()//2)
        self.select_img_input_btn.clicked.connect(lambda: self.openFileDialog("file"))


        self.select_folder_input_btn = qtw.QPushButton("Folder")
        self.select_folder_input_btn.setFont(qtg.QFont("Poppins"))
        self.select_folder_input_btn.setFixedWidth(self.save_at_input.widthMM()//2)
        self.select_folder_input_btn.clicked.connect(lambda: self.openFileDialog("folder"))
    
        self.btn_container.addWidget(self.select_img_input_btn)
        self.btn_container.addWidget(self.select_folder_input_btn)

        # self.select_img_input_btn.mousePressEvent = lambda event: self.verifyInputValue("select_img_input_btn")
        # self.select_img_input_btn.mousePressEvent = self.check_input_event
        # Create Checkboxes
        autoscan_checkbox = qtw.QCheckBox("Escaneamento automático:")
        autoscan_checkbox.setFont(qtg.QFont("Poppins Medium", 9))

        smart_correction_checkbox = qtw.QCheckBox("Aprimoramento inteligente")
        smart_correction_checkbox.setFont(qtg.QFont("Poppins Medium", 9))

        checkbox_stylesheet = """
            QCheckBox {
                spacing: 5px;
                color: #D94E16;
                text-decoration: underline;
                padding-top:10px;
            }
            QCheckBox::indicator {
                
                width: 20px;
                height: 20px;
            }
        """
        autoscan_checkbox.setStyleSheet(checkbox_stylesheet)
        smart_correction_checkbox.setStyleSheet(checkbox_stylesheet)

        self.start_button = qtw.QPushButton("Começar")
        self.start_button.setFont(qtg.QFont("Poppins Semibold", 16))
        self.start_button.setStyleSheet("background-color:#D94E16; border-radius:4px; border:none; color:white")
        self.start_button.setFixedHeight(44)
        self.start_button.setMaximumWidth(360)
        self.start_button.clicked.connect(self.on_button_clicked)

        ### POSITIONING INSIDE LAYOUTS
        ## LEFT FRAME
        main_layout.addWidget(self.left_frame_stacker, 6)
        main_layout.addWidget(self.right_frame, 4)

        self.left_frame_stacker.addWidget(self.left_frame_init)
        self.left_frame_stacker.addWidget(self.left_frame_list)
        self.left_frame_stacker.addWidget(self.left_frame_alt)



        self.left_frame_init_layout.addWidget(logo_img)
        self.left_frame_init_layout.addWidget(logo_subtitle)
        self.left_frame_init_layout.addSpacerItem(qtw.QSpacerItem(0,24))

        self.left_frame_init_layout.addWidget(self.drag_n_drop_container)
        self.dnd_container_layout.addWidget(self.drag_n_drop_rectangle)

        drag_n_drop_inner_layout.addWidget(drag_n_drop_label_txt)
        drag_n_drop_inner_layout.addWidget(drag_n_drop_hypertxt)
        drag_n_drop_inner_layout.addSpacerItem(qtw.QSpacerItem(0,24))
        drag_n_drop_inner_layout.addWidget(upload_files_folder_icon, alignment=qtc.Qt.AlignmentFlag.AlignHCenter)

        #VARIATION


        self.img_display = qtw.QLabel()
        self.img_display.setMinimumWidth(self.left_frame_stacker.width())
        self.img_display.setMinimumHeight(self.left_frame_stacker.height())
        self.img_display.setStyleSheet("background-color: red")

        self.img_ratio = self.img_display.height() / self.img_display.width()


        self.height_scaled = self.left_frame_stacker.height()
        self.width_scaled = int(self.height_scaled * self.img_ratio)

        self.current_img = r"C:/Users/Apollo/Desktop/Scanner.py/input_folder/2.jpg"
        self.pixmap = qtg.QPixmap(self.current_img)
        self.scaled_pixmap = self.pixmap.scaledToWidth(self.width_scaled, qtc.Qt.TransformationMode.SmoothTransformation)

        self.img_display.setPixmap(self.scaled_pixmap)
        # print(scaled_pixmap.width(), scaled_pixmap.height())
      



        self.left_frame_alt_layout.addWidget(self.img_display)


        ## RIGHT FRAME
        self.right_frame_layout.addWidget(self.select_img_input_btn_label)
        self.right_frame_layout.addLayout(self.btn_container)
        self.right_frame_layout.addSpacerItem(qtw.QSpacerItem(0, 24))
        self.right_frame_layout.addWidget(self.save_at_input_label)
        self.right_frame_layout.addWidget(self.save_at_input)
        self.right_frame_layout.addWidget(autoscan_checkbox)
        self.right_frame_layout.addWidget(smart_correction_checkbox)
        self.right_frame_layout.addSpacerItem(qtw.QSpacerItem(0, 100))
        self.right_frame_layout.addWidget(self.start_button)
        

    # def resizeEvent(self, event):
    #     print(f'Stacker-width: {self.left_frame_stacker.width()}, Stacker-height: {self.left_frame_stacker.height()}')
    #     print(f'left-frame-init-width: {self.left_frame_init.width()}, left-frame-init-height: {self.left_frame_init.height()}')
    #     print(f'left-frame-alt-width: {self.left_frame_alt.width()}, left-frame-alt-height: {self.left_frame_alt.height()}')


        # LAYOUT CONFIG

        # switch_button = qtw.QPushButton('Alternar Layout')
        # switch_button.clicked.connect(self.switchLayout)
        # main_layout.addWidget(switch_button)

    # FUNCTIONALITIES
    def set_single_step(self):
        self.left_frame_list.verticalScrollBar().setSingleStep(self.spinbox.value())


        self.resizeEvent = self.resizeEvent

    # def resizeEvent(self, event):
    #     self.left_frame_stacker.setMaximumWidth(int(self.width() * 0.6))
    #     self.left_frame_init.setFixedWidth(self.left_frame_stacker.width())
    #     self.left_frame_alt.setFixedWidth(self.left_frame_stacker.width())
    #     if self.width() > 1024:
    #         self.left_frame_stacker.setMaximumWidth(int(self.width() * 0.5))

    #     self.img_display.setFixedHeight(self.height())
    #     self.img_display.setFixedWidth(int(self.width()*0.6))
    #     self.height_scaled = self.img_display.height()
    #     self.width_scaled = int(self.height_scaled * self.img_ratio)
    #     self.scaled_pixmap = self.pixmap.scaledToWidth(self.width_scaled, qtc.Qt.TransformationMode.SmoothTransformation)
    #     self.img_display.setPixmap(self.scaled_pixmap)
    #     # if self.img_display.width() <= self.img_display.height():

    #     #     print("yeah")
    #     #     self.img_display.setFixedWidth(self.left_frame_alt.width())
    #     #     self.img_display.setFixedHeight(self.left_frame_alt.height())


    #     # else: 
    #     #     pass

    #     self.select_img_input_btn.mousePressEvent = self.check_input_event
    
  
    # def check_input_event(self, event):
    #     if self.selected_files == []:
    #         self.openFileDialog(self)
    #     else:
    #         pass


    # def displayDropDown(self, event):
    #     if self.selected_files == []:
    #         self.on_button_clicked(self.select_img_input_btn)
    #         # self.select_img_input_btn.setStyleSheet(""" QComboBox {background-color: red;} """)
    #     else:
    #        self.select_img_input_btn.setStyleSheet(""" QComboBox {background-color: green;} """)


    def switchLeftFrame(self, frame):
        if frame == "home":
            self.left_frame_stacker.setCurrentIndex(0)

        if frame == "list":
            self.left_frame_stacker.setCurrentIndex(1)

        if frame == "work":
            self.left_frame_stacker.setCurrentIndex(2)

        if frame == "result":
            self.left_frame_stacker.setCurrentIndex(3)



        # current_index = self.left_frame_stacker.currentIndex()
        # new_index = (current_index + 1) % self.left_frame_stacker.count()
        # self.left_frame_stacker.setCurrentIndex(new_index)



    def changeCursorToHand(self, event):
            self.setCursor(qtc.Qt.CursorShape.PointingHandCursor)


    def changeCursorToArrow(self, event):
            self.setCursor(qtc.Qt.CursorShape.ArrowCursor)

    def openDir(self, event):
            self.save_at_path = qtw.QFileDialog.getExistingDirectory(self, "Select Directory")
            self.save_at_input.setText(self.save_at_path)


    # def verifyInputValue(self, element):
    #     if element == "save_at_input" and self.save_at_input.text() == "":
    #         self.openDir(self)

    #     elif element == "select_img_input_btn" and self.count == 0:
    #         self.openFileDialog(self)

    #     elif self.count != 0:
    #         self.select_img_input_btn.mousePressEvent = None

    #     else:
    #         print("It has value")

    def on_button_clicked(self, event):
        self.switchLeftFrame("work")
        try:
            if self.selected_files != []:
                    file_path = self.selected_files
                    file_path = file_path[0]
                    ManualImageWarper(self.current_img, file_path, self)

            elif self.selected_folder != []:
                    file_path = self.selected_folder
                    file_path = file_path[0]
                    ManualImageWarper(self.current_img, file_path, self)

            else:
                    print("Select a file first.")
                    file_path = ""
        except: 
             print("error")
                    




    def addToList(self, element):
        self.select_img_input_btn.addItem(element)


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            filename = os.path.basename(f)
            self.addToList(filename)

    def openFileDialog(self, type):
        if type == "file":
            file_dialog = qtw.QFileDialog(self)
            file_dialog.setWindowTitle("Select a file")
            file_dialog.setFileMode(qtw.QFileDialog.FileMode.ExistingFiles)

            if file_dialog.exec() == qtw.QDialog.DialogCode.Accepted:
                self.switchLeftFrame("list")
                self.selected_files = file_dialog.selectedFiles()
                print(self.selected_files)

                for file_path in self.selected_files:
                    file_name = os.path.basename(file_path)
                    self.file_var_name = self.replace_numbers_with_letters(os.path.splitext(file_path)[0]) #converts numbers in letters and sets the variables
                    self.count += 1
                    pixmap = qtg.QPixmap(file_path).scaled(128, 128, qtc.Qt.AspectRatioMode.KeepAspectRatio, qtc.Qt.TransformationMode.SmoothTransformation)
                    icon = qtg.QIcon(pixmap)

                    self.file_list_item = qtw.QListWidgetItem(icon, file_name)
                    self.file_list_item.setToolTip(file_path)
                    self.file_list_item.setSizeHint(qtc.QSize(144, 144))
                    self.left_frame_list.addItem(self.file_list_item)

                # Do something with selected_files
        if type == "folder":
            folder_dialog = qtw.QFileDialog(self)
            folder_dialog.setWindowTitle("Select a folder")
            folder_dialog.setFileMode(qtw.QFileDialog.FileMode.Directory)

            if folder_dialog.exec() == qtw.QDialog.DialogCode.Accepted:
                self.switchLeftFrame("list")
                self.selected_folder =  folder_dialog.selectedFiles()[0]
                self.selected_files = os.listdir(self.selected_folder)
                
                
                


                for file_path in self.selected_files:
                    file_name = os.path.basename(file_path)
                    self.file_var_name = self.replace_numbers_with_letters(os.path.splitext(file_path)[0]) #converts numbers in letters and sets the variables
                    self.count += 1
                    pixmap = qtg.QPixmap(file_path).scaled(128, 128, qtc.Qt.AspectRatioMode.KeepAspectRatio, qtc.Qt.TransformationMode.SmoothTransformation)
                    icon = qtg.QIcon(pixmap)

                    self.file_list_item = qtw.QListWidgetItem(icon, file_name)
                    self.file_list_item.setToolTip(file_path)
                    self.file_list_item.setSizeHint(qtc.QSize(144, 144))
                    self.left_frame_list.addItem(self.file_list_item)
           
                    



   

                # for file in os.listdir(path):
                # full_path = os.path.abspath(os.path.join(path, file)) 

                # pixmap = qtg.QPixmap(full_path).scaled(128, 128, qtc.Qt.AspectRatioMode.KeepAspectRatio, qtc.Qt.TransformationMode.SmoothTransformation)

                # icon = qtg.QIcon(pixmap)



        # except Exception as e:
        #     print(f"An error occurred: {e}")
        # pass

    def replace_numbers_with_letters(self, sentence):
        result = ''
        for char in sentence:
            if char.isdigit():
                # Convert digit to corresponding letter of the alphabet
                letter = chr(ord('a') + int(char) - 1)
                result += letter
            else:
                result += char
        return result
    


        








if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mainWindow = MainWindow()

    mainWindow.show()
    sys.exit(app.exec())
