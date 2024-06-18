from PIL import Image

def split_image_by_height(image_path, height_in_px):
    """
    根据指定的高度将图片分割成多部分
    :param image_path: 图片文件路径
    :param height_in_px: 每个分割部分的高度（以像素为单位）
    """
    with Image.open(image_path) as img:
        width, original_height = img.size
        # 计算需要分割的行数
        rows = (original_height + height_in_px - 1) // height_in_px
        
        # 分割图片
        index = 15
        for i in range(rows):
            # 计算裁剪坐标
            upper = i * height_in_px
            lower = min((i + 1) * height_in_px, original_height)
            box = (0, upper, width, lower)
            # 裁剪小图
            crop_img = img.crop(box)
            # 保存小图或进行进一步处理
            crop_img.save(f'./2pdf/page_{index + i + 1}.png')

# 使用例子
# 假设图片宽度是700px，你希望每个分割部分的高度为500px
split_image_by_height('C:\\Users\\syske\\Downloads\\W020240410312339010259.png', 921)