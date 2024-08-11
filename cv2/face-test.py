import cv2 as cv

img = cv.imread('./face2.jpg')
# 指定图像大小
img_resize = cv.resize(img,dsize=(700,700))

# 定义检测函数
def test():
  #定义级联分类器的路径
    face_test =cv.CascadeClassifier('D:/dev-tool/python/py3.10.10/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')
    #对图像进行检测，1.01为检测的倍数，5为检测次数，0为默认参数，后面两个为最小检测范围和最大检测范围为100*100和300*300像素
    face = face_test.detectMultiScale(img_resize,1.05,5,0,(30,30),(300,300))
    for x,y,w,h in face:
        cv.rectangle(img_resize,(x,y),(x+w,y+h),color = (0,255,0),thickness=2)
    cv.imshow('LYF',img_resize)

test()
# 空格退出
cv.waitKey(0)
# 释放内存
cv.destroyAllWindows()