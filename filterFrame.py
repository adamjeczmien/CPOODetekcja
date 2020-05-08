import cv2
import numpy as np
def filterFrame(frame):
    kernel_sharpening = np.array([[-1,-1,-1],
                              [-1, 9,-1],
                              [-1,-1,-1]])
    median_blur = cv2.medianBlur(frame, 15)
    sharpened = cv2.filter2D(median_blur, -1, kernel_sharpening)
    return sharpened