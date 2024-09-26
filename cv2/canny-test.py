import cv2
import numpy as np

# 加载图像
image = cv2.imread('face1.jpeg')

# 转换为灰度图像
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 应用高斯模糊减少噪声
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Canny边缘检测
edges = cv2.Canny(blurred, threshold1=50, threshold2=150)

# 显示原图与边缘检测后的结果
cv2.imshow('Original Image', image)
cv2.imshow('Edges', edges)

# 等待按键后关闭窗口
cv2.waitKey(0)
cv2.destroyAllWindows()