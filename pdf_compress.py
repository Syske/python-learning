import os
import PyPDF2
import fitz  # PyMuPDF


# ---------------------------------------逐页压缩，效果未知-------------------------------------
def compress_by_page(path1, path2):
    """
    :param path1: 需要压缩的pdf文件路径
    :param path2: 保存的pdf文件路径
    :return: None
    逐页压缩，效果未知，慢！！！
    """
    pdf_file = open(path1, "rb")
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    pdf_writer = PyPDF2.PdfWriter()
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        page.compress_content_streams()
        pdf_writer.add_page(page)
    out_file = open(path2, "wb")
    pdf_writer.write(out_file)
    out_file.close()
    pdf_file.close()

def compress_pdf_pymupdf(input_path, output_path):
    # 打开PDF文件
    doc = fitz.open(input_path)
    
    # 压缩PDF
    doc.save(output_path, garbage=4, deflate=True, clean=True)


if __name__ == "__main__":
    in_path = 'C:\\Users\\syske\\Documents\\WeChat Files\\qq_715448004\\FileStorage\\File\\2024-08\\27.pdf'  # 需要压缩的PDF文件
    out_path = "321.pdf"  # 压缩后的PDF文件路径
#    compress_by_page(in_path, out_path)
    compress_pdf_pymupdf(in_path, out_path)