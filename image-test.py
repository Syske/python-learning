import PIL
from PIL import Image

target_long_side_pixe=6000
input_pic = "./DSC_0458.JPG"
output_pic = "./test.jpeg"
output_pic_format = "JPEG"


image = Image.open(input_pic, mode='r')
print(f'format={image.format}, fromat_description={image.format_description}, size={image.size}')

maxValue = max(image.size)
maxType = image.size.index(maxValue)


if maxType == 0:
    image.thumbnail(
        (target_long_side_pixe, image.size[0] * (image.size[1]/target_long_side_pixe)))
if maxType == 1:
    image.thumbnail(
        (image.size[0] * (image.size[1]/target_long_side_pixe), target_long_side_pixe))
print(f'image save size ={image.size}')
image.save(output_pic, output_pic_format)
