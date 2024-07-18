import cv2

# 读取图片
img = cv2.imread('../2pdf/page_1.png', cv2.IMREAD_GRAYSCALE)

# 显示图像
cv2.imshow('image', img)
# 没有这个窗口会直接关闭
cv2.waitKey(0)