import PyPDF2
from PIL import Image
file_path = "D:\\workspace\\个人文件"
# 打开要签字的PDF文件并创建PDF reader对象
pdf_file = open(f'{file_path}\\民事起诉状.pdf', 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)

# 获取第一页的PDF page对象
page = pdf_reader.pages[1]

# 打开要签字的图片文件并转换为PDF兼容的格式
signature_image = Image.open(f'{file_path}\\sign-leicao.png')
signature_image = signature_image.convert('RGB')

# 创建PDF模板对象并设置签名的位置和大小
template = page.extract_text_box()
template.rect.x = 100  # 签名的x坐标
template.rect.y = 500   # 签名的y坐标
template.rect.width = 200  # 签名的宽度
template.rect.height = 100  # 签名的的高度

# 将签名图片转换为PDF兼容的格式并添加到PDF模板中
signature_image_pdf = PyPDF2.utils.ImageReader(signature_image.fp)
template.merge(signature_image_pdf, template.rect)

# 创建PDF writer对象并写入输出PDF文件
pdf_writer = PyPDF2.PdfFileWriter()
pdf_writer.addPage(template)
output_pdf = open(f'{file_path}\\output.pdf', 'wb')
pdf_writer.write(output_pdf)

# 关闭文件
pdf_file.close()
output_pdf.close()
