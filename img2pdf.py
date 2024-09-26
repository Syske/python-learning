from PIL import Image
from fpdf import FPDF
import os
import io
import tempfile

import img2pdf

def image_to_pdf(image_path, output_path):
    # 将图像转换为PDF
    with open(output_path, "wb") as f:
        f.write(img2pdf.convert(image_path))
        


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
            pdf_width = img_width
            pdf_height = img_height
            print(img_width, img_height)
            # 将图片添加到PDF中，每个图片一页
            pdf.add_page()
            pdf.image(image_path, x=0, y=0, w=pdf_width, h=pdf_height)
    
    # 保存PDF文件
    pdf.output(output_pdf, "F")
    
class ImageToPDF(FPDF):
    def __init__(self):
         super().__init__(unit='pt')  # 设置单位为点
        self.set_auto_page_break(auto=True, margin=15)

    # 1英寸 = 25.4毫米
    # 如果分辨率是72 DPI，那么1像素 = 25.4 mm / 72 pixels ≈ 0.352777778 mm
    # 如果分辨率是300 DPI，那么1像素 = 25.4 mm / 300 pixels ≈ 0.084666667 mm
    
    # 1点 = 1/72英寸
    # 如果分辨率是72 DPI，那么1像素 = 1点
    # 如果分辨率是300 DPI，那么1像素 = 1/300 * 72 ≈ 0.24点
    def add_image(self, image_path):
        # 打开图像文件并获取尺寸
        img = Image.open(image_path)
        width, height = img.size
        dpi = img.info.get('dpi')
        # 如果没有DPI信息，则默认为72 DPI
        if dpi is None:
          dpi = 72
        print(dpi, img.size)
        # 创建一个临时的PDF实例，设置页面大小
        temp_pdf = FPDF(unit='pt', format=(int(width / (dpi[0] / 72)), int(height / (dpi[1] / 72))))
        print()
        temp_pdf.add_page()
        temp_pdf.set_margins(0, 0, 0)
        temp_pdf.set_auto_page_break(auto=False)
        temp_pdf.image(image_path, x=0, y=0, w=width, h=height)
        
        # 将临时PDF实例的内容合并到主PDF实例中
        # temp_pdf_output = io.BytesIO()
        # temp_pdf.output(temp_pdf_output, 'F')
        # temp_pdf_output.seek(0)
        return temp_pdf
        # 创建一个临时文件
#         with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
#             tmpfile.write(temp_pdf_output.getvalue())
            
#             # 使用临时文件作为源文件
#             self.set_source_file(tmpfile.name)
#             temp_pdf_import = self.import_page(1)
#             self.add_page()
#             self.use_template(temp_pdf_import)
        
def single_image_to_pdf(image_path, output_path):
    pdf = ImageToPDF()
    temp_pdf_output = pdf.add_image(image_path)
    temp_pdf_output.output(output_path)

# 使用示例
#images_to_merge = ['image1.jpg', 'image2.jpg', 'image3.jpg']  # 图片文件路径列表
images_to_merge = os.listdir('C:\\Users\\syske\\Documents\\WeChat Files\\qq_715448004\\FileStorage\\File\\2024-08\\27')
#print(type(images_to_merge))

for i in range(len(images_to_merge)):
    images_to_merge[i] =  f'C:\\Users\\syske\\Documents\\WeChat Files\\qq_715448004\\FileStorage\\File\\2024-08\\27\\{i + 1}.png'
output_file = 'merged.pdf'  # 输出PDF文件的路径
#images_to_pdf(images_to_merge, output_file)
# 使用函数
image_path = 'C:\\Users\\syske\\Documents\\WeChat Files\\qq_715448004\\FileStorage\\File\\2024-08\\27\\1.png'  # 更改为你的图像文件路径
output_pdf = 'output.pdf'  # 更改为你要保存的PDF文件路径
single_image_to_pdf(image_path, output_pdf)