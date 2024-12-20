import fitz
import os

def convert_pdf2img(file_relative_path):
    
     """

     file_relative_path : 文件相对路径

     """

     page_num = 1

     filename = file_relative_path.split('.')[-2]

     if not os.path.exists(filename):

          os.makedirs(filename)

     pdf = fitz.open(file_relative_path)

     for page in pdf:

          rotate = int(0)

          # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高4的图像。

          # 此处若是不做设置，默认图片大小为：792X612, dpi=96

          zoom_x = 2 # (2-->1584x1224)

          zoom_y = 2

          mat = fitz.Matrix(zoom_x, zoom_y)

          pixmap = page.get_pixmap(matrix=mat, alpha=False)

          pixmap.pil_save(f"{filename}/{page_num}.png")

          print(f"{filename}.pdf 第{page_num}页保存图片完成")

          page_num = page_num + 1


if __name__ =="__main__":
    file = 'C:\\Users\\syske\\Documents\\WeChat Files\\qq_715448004\\FileStorage\\File\\2024-08\\27.pdf'
     # 文件夹中文件名
    convert_pdf2img(file)