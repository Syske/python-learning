import cv2
import numpy as np
import imutils
import os



img = cv2.imread('P60820-140738(1).jpg', 1)
cv2.imshow('img',  imutils.resize(img, 800))
img = cv2.resize(img, None, fx=1, fy=1)
rows, cols, channels = img.shape
print(f"img info rows = {rows}, cols = {cols}, channels = {channels}")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow('hsv', imutils.resize(hsv, 800))

lower_blue = np.array([90, 70, 70])
upper_blue = np.array([110, 255, 255])
# 蓝色范围内变白，其余之外全部变黑
mask = cv2.inRange(hsv, lower_blue, upper_blue)

erode = cv2.erode(mask, None, iterations=1)
dilate = cv2.dilate(mask, None, iterations=1)
cv2.imshow('dilate',  imutils.resize(dilate, 800))

for i in range(rows):
  for j in range(cols):
    if dilate[i, j] == 255: # 获取图片中的像素点
      img[i, j] = (0, 0, 255)

cv2.imshow('end',  imutils.resize(img, 800))
# 没有如下两行代码，图片不显示
cv2.waitKey(0)
cv2.destroyAllWindows()