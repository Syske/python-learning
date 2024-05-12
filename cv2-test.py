import cv2
import numpy as np
import imutils
import os



gray_img = cv2.imread('Snipaste_2022-10-12_09-23-47.jpg', 0)
blur = cv2.GaussianBlur(gray_img, (3, 3), 0)
canny = cv2.Canny(blur, 50, 150)
canny2 = cv2.Canny(gray_img, 50, 150)

cv2.imshow('gray_img', gray_img)
cv2.imshow('blur', blur)
cv2.imshow('canny', canny)
cv2.imshow('canny2', canny2)
# 没有如下两行代码，图片不显示
cv2.waitKey(0)
cv2.destroyAllWindows()