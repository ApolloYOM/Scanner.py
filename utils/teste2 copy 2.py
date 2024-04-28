import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt6.QtGui import QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt, QPoint

class CircleLabel(QLabel):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.setFixedSize(32, 32)
        self.dragging = False
        self.offset = QPoint()
        self.setPixmap(QPixmap(image_path))

    def mousePressEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(self.mapToParent(event.pos() - self.offset))

    def mouseReleaseEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.dragging = False

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle('Moving Circles')
        self.setStyleSheet("background-color: #000;")

        self.circle_labels = []
        image_path = "./assets/img/circle.svg"  # Use the same image for all circles

        positions = [(32, 32), (self.width() - 64, 32), (self.width() - 64, self.height() - 64), (32, self.height() - 64)]

        for position in positions:
            circle_label = CircleLabel(image_path, self)
            circle_label.move(*position)
            self.circle_labels.append(circle_label)

        self.button = QPushButton('Get Coordinates', self)
        self.button.setGeometry(200, 400, 120, 40)
        self.button.clicked.connect(self.get_coordinates)

    def get_coordinates(self):
        print("Circle Coordinates:")
        for circle_label in self.circle_labels:
            print(circle_label.pos().x(), circle_label.pos().y())

def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
