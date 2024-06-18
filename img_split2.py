from PIL import Image

def split_image_to_a4_pages(image_path, a4_size_mm=(210, 297), resolution=300):
    """
    将图片按照A4纸张大小等比例缩放并分割成多个页面
    :param image_path: 图片文件路径
    :param a4_size_mm: A4纸张尺寸，单位毫米，默认为(210, 297)
    :param resolution: 输出分辨率，单位dpi，默认为300
    """
    # 将A4纸张尺寸从毫米转换为像素
    a4_size_px = tuple(round(size * resolution / 25.4) for size in a4_size_mm)

    # 打开图片并获取原始尺寸
    with Image.open(image_path) as img:
        original_width, original_height = img.size

        # 计算缩放比例
        scale_width = a4_size_px[0] / original_width
        scale_height = a4_size_px[1] / original_height
        scale = min(scale_width, scale_height)  # 选择较小的比例以保持等比例缩放

        # 计算缩放后的图片尺寸
        scaled_width = int(original_width * scale)
        scaled_height = int(original_height * scale)

        # 创建缩放后的图片
        scaled_img = img.resize((scaled_width, scaled_height), Image.ANTIALIAS)

        # 计算分割的页面数量（向上取整）
        pages_width = -(-scaled_width // a4_size_px[0])  # 使用向上取整的技巧
        pages_height = -(-scaled_height // a4_size_px[1])

        # 分割图片并保存每个页面
        for page_y in range(pages_height):
            for page_x in range(pages_width):
                left = page_x * a4_size_px[0]
                upper = page_y * a4_size_px[1]
                right = min((page_x + 1) * a4_size_px[0], scaled_width)
                lower = min((page_y + 1) * a4_size_px[1], scaled_height)

                box = (left, upper, right, lower)
                page_img = scaled_img.crop(box)
                page_img.save(f'page_{page_x}_{page_y}.png')

# 使用示例
split_image_to_a4_pages('C:\\Users\\syske\\Downloads\\W020240410312339010259.png')