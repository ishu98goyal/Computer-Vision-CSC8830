import cv2
import numpy as np
image = cv2.imread('pic.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite('pic_gray.jpg', gray)