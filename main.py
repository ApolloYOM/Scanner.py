import sys
from PyQt6.QtWidgets import QApplication
from utils.gui import MainWindow
# from utils.scanner.auto_warp import Scanner
from utils.scanner.manual_warp import ManualImageWarper  

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    # scanner = Scanner()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
