from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QImage, QPainter
from PyQt6.QtCore import Qt, QPoint
import numpy as np
import cv2
import os
import sys

class ManualImageWarper(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.img = cv2.imread(image_path)
        self.h, self.w, _ = self.img.shape
        a_ratio = self.w / self.h
        self.h_resized = 640
        self.w_resized = int(self.h_resized * a_ratio)
        self.p_ratio = self.h / self.h_resized
        self.img_resized = cv2.resize(self.img, (self.w_resized, self.h_resized))
        self.circle_size = 6
        circle_w = self.circle_size * 2
        self.circles = [
            [0 + circle_w, 0 + circle_w],
            [self.w_resized - circle_w, 0 + circle_w],
            [0 + circle_w, self.h_resized - circle_w],
            [self.w_resized - circle_w, self.h_resized - circle_w]
        ]
        self.active_circle = None
        self.offset_x = 0
        self.offset_y = 0

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color:red")
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.image_label = QLabel()
        self.update_image()

        layout.addWidget(self.image_label)

        self.setWindowTitle('Manual Image Warper')
        self.show()

    def update_image(self):
        img_with_circles = self.img_resized.copy()
        self.draw_circles(img_with_circles, self.active_circle)
        self.draw_lines(img_with_circles)
        q_img = self.convert_cv_to_qt(img_with_circles)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))
        print("up")

    def convert_cv_to_qt(self, cv_img):
        height, width, channel = cv_img.shape
        bytes_per_line = 3 * width
        q_image = QImage(cv_img.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
        return q_image

    def draw_circles(self, img, active_circle=None):
        for i, circle in enumerate(self.circles):
            color = (0, 0, 255) if i != active_circle else (255, 0, 0)
            cv2.circle(img, (circle[0], circle[1]), self.circle_size, color, -1)
            cv2.putText(img, str(i + 1), (circle[0] - 10, circle[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    def draw_lines(self, img):
        connections = [(0, 1), (1, 3), (3, 2), (2, 0)]
        for conn in connections:
            cv2.line(img, (self.circles[conn[0]][0], self.circles[conn[0]][1]),
                     (self.circles[conn[1]][0], self.circles[conn[1]][1]), (0, 255, 0), 2)

    def point_in_circles(self, point):
        for i, circle in enumerate(self.circles):
            distance = np.sqrt((point[0] - circle[0]) ** 2 + (point[1] - circle[1]) ** 2)
            if distance <= self.circle_size * 2:
                return i
        return None

    def warp_perspective(self):
        pts1 = np.float32(self.reorder(np.array([[point[0] * self.p_ratio, point[1] * self.p_ratio] for point in self.circles])))
        pts2 = np.float32([[0, 0], [self.w, 0], [0, self.h], [self.w, self.h]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        img_output = cv2.warpPerspective(self.img, matrix, (self.w, self.h))
        return img_output

    def reorder(self, my_points):
        my_points = my_points.reshape((4, 2))
        my_points_new = np.zeros((4, 1, 2), dtype=np.int32)
        add = my_points.sum(1)
        my_points_new[0] = my_points[np.argmin(add)]
        my_points_new[3] = my_points[np.argmax(add)]
        diff = np.diff(my_points, axis=1)
        my_points_new[1] = my_points[np.argmin(diff)]
        my_points_new[2] = my_points[np.argmax(diff)]
        return my_points_new

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Return:
    #         if all(circle is not None for circle in self.circles):
    #             img_warped = self.warp_perspective()
    #             cv2.imshow('Warped Image', img_warped)
    #             cv2.waitKey(0)
    #             cv2.destroyWindow('Warped Image')

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()
            for i, circle in enumerate(self.circles):
                center_x, center_y = circle
                distance_squared = (mouse_pos.x() - center_x) ** 2 + (mouse_pos.y() - center_y) ** 2
                if np.sqrt(distance_squared) <= 16:
                    self.active_circle = i
                    self.dragging_offset = mouse_pos - QPoint(center_x, center_y)
                    break
            self.update_image()

    def mouseMoveEvent(self, event):
        if self.active_circle is not None:
            mouse_pos = event.pos()
            new_center = mouse_pos - self.dragging_offset
            self.circles[self.active_circle] = [new_center.x(), new_center.y()]
            self.update_image()

    def mouseReleaseEvent(self, event):
        self.active_circle = None
        self.update_image()

    def closeEvent(self, event):
        cv2.destroyAllWindows()
        event.accept()

if __name__ == "__main__":
    app = QApplication([])
    warper = ManualImageWarper("C:/Users/Apollo/Desktop/Scanner.py/input_folder/1.jpg")
    sys.exit(app.exec())
