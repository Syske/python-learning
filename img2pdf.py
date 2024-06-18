from PIL import Image
from fpdf import FPDF
import os

def images_to_pdf(images_paths, output_pdf):
    """
    将多个图片合并成一个PDF文件，每个图片占据一页。
    :param images_paths: 图片文件路径列表
    :param output_pdf: 输出PDF文件的路径
    """
    pdf = FPDF()
    
    for image_path in images_paths:
        with Image.open(image_path) as img:
            # 获取图片尺寸
            img_width, img_height = img.size
            # 将图片尺寸转换为PDF单位（毫米），假设分辨率为72dpi
            pdf_width = img_width / 85 * 25.4
            pdf_height = img_height / 85 * 25.4
            
            # 将图片添加到PDF中，每个图片一页
            pdf.add_page()
            pdf.image(image_path, x=0, y=0, w=pdf_width, h=pdf_height)
    
    # 保存PDF文件
    pdf.output(output_pdf, "F")

# 使用示例
#images_to_merge = ['image1.jpg', 'image2.jpg', 'image3.jpg']  # 图片文件路径列表
images_to_merge = os.listdir('./2pdf')
#print(type(images_to_merge))

for i in range(len(images_to_merge)):
    images_to_merge[i] =  f'./2pdf/page_{i + 1}.png'
output_file = 'merged.pdf'  # 输出PDF文件的路径
images_to_pdf(images_to_merge, output_file)