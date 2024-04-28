import cv2
import numpy as np
import os
import imutils
import utils.scanner.utlis as utlis
from PIL import Image
from win32api import GetSystemMetrics


    # for img_path in selected_imgs:
    #     if img_path.lower().endswith('.heic'):
    #         print(f"O arquivo {img_path} tem a extensão .heic")
    #         print("Converter para png")
    #     else:
    #         print(f"O arquivo {img_path} não tem a extensão .heic")

def scan():
    img = cv2.imread("./input_folder/1.jpg")
    h, w, _ = img.shape
    imgBlank = np.zeros((h,w, 3), np.uint8)# CREATE A BLANK IMAGE FOR TESTING DEBUGING IF REQUIRED
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgThreshold = cv2.Canny(imgBlur, 90, 90) # APPLY CANNY BLUR
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgThreshold, kernel, iterations=2) # APPLY DILATION
    imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # APPLY EROSION

    ## FIND ALL COUNTOURS
    imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
    cv2.drawContours(imgContours, contours, -1, (0, 255, 255), 32) # DRAW ALL DETECTED CONTOURS


    # FIND THE BIGGEST COUNTOUR
    biggest, maxArea = utlis.biggestContour(contours) # FIND THE BIGGEST CONTOUR
    if biggest.size != 0:
        biggest=utlis.reorder(biggest)
        imgBigContour = utlis.drawRectangle(imgBigContour,biggest, 48)
        cv2.drawContours(imgBigContour, biggest, -1, (0, 0, 255), 80) # DRAW THE BIGGEST CONTOUR

        pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
        pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)

        imgWarpColored = cv2.warpPerspective(img, matrix, (w, h))

        # REMOVE 20 PIXELS FORM EACH SIDE
        imgWarpColored=imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
        imgWarpColored = cv2.resize(imgWarpColored,(w,h))

        # APPLY ADAPTIVE THRESHOLD
        imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
        imgAdaptiveThre= cv2.adaptiveThreshold(imgWarpGray, 255, 1, 1, 7, 2)
        imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
        imgAdaptiveThre=cv2.medianBlur(imgAdaptiveThre,7)

        #Display Config
        sHeight = round(GetSystemMetrics(1)/2)-32
        print(sHeight)
        d_img = imutils.resize(img, height=sHeight)
        d_imgGray = imutils.resize(imgGray, height=sHeight)
        d_imgThreshold = imutils.resize(imgThreshold, height=sHeight)
        d_imgWarpGray = imutils.resize(imgWarpGray, height=sHeight)
        d_imgContours = imutils.resize(imgContours, height=sHeight)
        d_imgBigContour = imutils.resize(imgBigContour, height=sHeight)
        d_imgWarpColored = imutils.resize(imgWarpColored, height=sHeight)
        d_imgAdaptiveThre = imutils.resize(imgAdaptiveThre, height=sHeight)

        # Image Array for Display
        imageArray = ([d_img,d_imgGray,d_imgThreshold,d_imgContours],
                    [d_imgBigContour,d_imgWarpColored,d_imgWarpGray,d_imgAdaptiveThre])

    else:
        imageArray = ([d_img,d_imgGray,d_imgThreshold,d_imgContours],
                    [imgBlank, imgBlank, imgBlank, imgBlank])

    # LABELS FOR DISPLAY
    lables = [["Original","Gray","imgThreshold","Contours"],
            ["Biggest Contour","Warp Perspective","Warp Gray","Threshold"]]

    stackedImage = utlis.stackImages(imageArray,1,lables)

    cv2.imshow("Result", stackedImage)
        

                # key = cv2.waitKey(0) & 0xFF
                # if key == ord('s'):
                #     output_folder = "output_folder"
                #     os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist
                    
                #     # Extract the filename from the original image path
                #     original_filename = os.path.basename(file_path)
                    
                # # Append "_scanned" to the filename
                #     scanned_filename = original_filename.split('.')[0] + "_scanned." + original_filename.split('.')[-1]
                        
                #     # Construct the full output path
                #     output_path = os.path.join(output_folder, scanned_filename)
                    
                #     # Save the image
                #     cv2.imwrite(output_path, imgAdaptiveThre)

    cv2.waitKey(0)
    quit()
scan()

                # cv2.imshow("img", img)
                # cv2.imshow("GrayImg", GrayImg)
                # cv2.imshow("BlurredFrame", BlurredFrame)
                # cv2.imshow("CannyFrame", CannyFrame)
                # cv2.imshow("ContourFrame", ContourFrame)
                # cv2.imshow("CornerFrame", CornerFrame)
                # cv2.imshow("outputImage", imgWarp)
                # cv2.waitKey(0)

                # file_imgs = cv2.imread("image-input/" + file)
                # ratio = file_imgs.shape[0] / 640.0
                # w, h, _ = img.shape
