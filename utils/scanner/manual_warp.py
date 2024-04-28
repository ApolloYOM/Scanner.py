import cv2
import numpy as np
import imutils
import os

class ManualImageWarper:
    def __init__(self, image_path):
        self.img = cv2.imread(image_path)
        h, w, _ = self.img.shape
        self.new_h = 640
        self.new_w = self.new_h * w // h
        self.ratio = h/self.new_h
        self.img_resized = imutils.resize(self.img, self.new_w, self.new_h)
        self.circle_size = 6
        self.circles = [
            [0 + self.circle_size * 2, 0 + self.circle_size * 2],  # Upper left corner
            [self.new_w - self.circle_size * 2, 0 + self.circle_size * 2],  # Upper right corner
            [0 + self.circle_size * 2, self.new_h - self.circle_size * 2],  # Lower left corner
            [self.new_w - self.circle_size * 2, self.new_h - self.circle_size * 2]  # Lower right corner
        ]
        self.active_circle = None
        self.offset_x = 0
        self.offset_y = 0


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
            if distance <= self.circle_size * 1.5:
                return i
        return None

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.active_circle = self.point_in_circles((x, y))
            if self.active_circle is not None:
                self.offset_x = self.circles[self.active_circle][0] - x
                self.offset_y = self.circles[self.active_circle][1] - y

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.active_circle is not None:
                self.circles[self.active_circle][0] = x + self.offset_x
                self.circles[self.active_circle][1] = y + self.offset_y

        elif event == cv2.EVENT_LBUTTONUP:
            self.active_circle = None


    def warp_perspective(self):
        pts1 = np.float32(self.reorder(np.array([[point[0] * self.ratio, point[1] * self.ratio] for point in self.circles])))
        pts2 = np.float32([[0, 0], [self.img.shape[1], 0], [0, self.img.shape[0]], [self.img.shape[1], self.img.shape[0]]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        img_output = cv2.warpPerspective(self.img, matrix, (self.img.shape[1], self.img.shape[0]))
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
    def start(self):
        cv2.namedWindow('Drag And Drop')
        cv2.setMouseCallback('Drag And Drop', self.mouse_callback)

        while True:
            img_with_circles = self.img_resized.copy()

            self.draw_circles(img_with_circles, self.active_circle)
            self.draw_lines(img_with_circles)

            cv2.imshow('Drag And Drop', img_with_circles)

            key = cv2.waitKey(1)

            if key == ord('q') or cv2.getWindowProperty('Drag And Drop', cv2.WND_PROP_VISIBLE) < 1:
                break
            elif ord('1') <= key <= ord('4'):
                self.active_circle = key - ord('1')

            elif key == 13:  # ASCII code for Enter key
                if all(circle is not None for circle in self.circles):
                    img_warped = self.warp_perspective()
                    img_show = imutils.resize(img_warped, height=self.new_h)
                    cv2.imshow('Warped Image', img_show)

            if key == ord('s'):
                output_folder = "output_folder"
                os.makedirs(output_folder, exist_ok=True)

                original_filename = os.path.basename("input_folder/3.png")
                scanned_filename = original_filename.split('.')[0] + "_scanned." + original_filename.split('.')[-1]
                output_path = os.path.join(output_folder, scanned_filename)

                cv2.imwrite(output_path, img_warped)
                cv2.waitKey(0)
                cv2.destroyWindow('Warped Image')

        cv2.destroyAllWindows()


if __name__ == "__main__":
    warper = ManualImageWarper("C:/Users/Apollo/Desktop/Scanner.py/input_folder/1.jpg")
    warper.start()