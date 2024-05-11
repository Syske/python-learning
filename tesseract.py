
import pytesseract
from PIL import Image
# 图片转文字
text = pytesseract.image_to_string(Image.open('123213.jpg'))