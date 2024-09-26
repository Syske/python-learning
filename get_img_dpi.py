from PIL import Image

def get_image_resolution(image_path):
    # 打开图像文件
    img = Image.open(image_path)
    
    # 获取分辨率
    dpi = img.info.get('dpi')
    
    # 如果没有DPI信息，则默认为72 DPI
    if dpi is None:
        dpi = 72
    
    return dpi

# 使用函数
image_path = 'C:/Users/syske/Documents/WeChat Files/qq_715448004/FileStorage/File/2024-08/27/1.png'  # 更改为你的图像文件路径
dpi = get_image_resolution(image_path)
print(f"The resolution of the image is {dpi} DPI.")