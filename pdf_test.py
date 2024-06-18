from PyPDF2 import PdfReader, PdfWriter

def split_pdf(file_path, output_prefix):
    pdf = PdfReader(file_path)
    output_pdf = PdfWriter()
    for page in pdf.pages:
        output_pdf.add_page(page)

    with open(output_prefix, "wb") as output_file:
        output_pdf.write(output_file)

# 使用函数来分割PDF
split_pdf('C:\\Users\\syske\\Downloads\\中国共产党纪律处分条例.pdf', 'C:\\Users\\syske\\Downloads\\中国共产党纪律处分条例2.pdf')