from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage,QClipboard
from PyQt5.QtCore import QTimer,QBuffer,QIODevice
from PIL import Image
import numpy as np
import sys,io

class ClipboardTool:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.clipboard = QApplication.clipboard()
        self.result = None

    def qimage_to_pil_image(self, qimage) -> Image.Image:
        
        img_bytes = self.qimage_to_bytes(qimage)
        image_file = io.BytesIO(img_bytes)
        pil_image = Image.open(image_file)
        return pil_image

    def process_clipboard(self):
        if self.clipboard.mimeData().hasImage():
            image = self.clipboard.image()
            if not image.isNull():
                try:
                    self.result = image
                except Exception as e:
                    print(e)
            else:
                print("剪贴板中的图片为空")
                self.result = None
        else:
            print("剪贴板中没有图片")
            self.result = None
        
        # 退出应用程序
        self.app.quit()
        
    def qimage_to_bytes(self, qimage: QImage) -> bytes:
        """
        将 QImage 转换为字节流
        """
        if not isinstance(qimage, QImage):
            print("Provided image is not a valid QImage object")
            raise ValueError("Provided image is not a valid QImage object")

        try:
            # 创建 QBuffer 对象
            buffer = QBuffer()
            buffer.open(QIODevice.WriteOnly)

            # 将 QImage 保存到 QBuffer 中
            success = qimage.save(buffer, "PNG")  # 保存为 PNG 格式
            if not success:
                print("Failed to save QImage to QBuffer")
                raise RuntimeError("Failed to save QImage to QBuffer")

            # 获取字节流
            image_bytes = buffer.data()
            buffer.close()
            print("QImage converted to bytes successfully")
            return image_bytes.data()
        except Exception as e:
            print(f"Error converting QImage to bytes: {e}")
            raise

    
    def get_clipboard_image(self) -> QImage:
        '''
        从剪贴板读取图片，返回类型QImage
        '''
        # 使用 QTimer 在 1 秒后调用 process_clipboard 函数
        QTimer.singleShot(0, self.process_clipboard)
        
        # 启动事件循环
        self.app.exec_()

        return self.result
    
    
    def get_clipboard_image_pil(self) -> Image.Image:
        image_bytes = self.get_clipboard_image_bytes()
        image_file = io.BytesIO(image_bytes)
        return Image.open(image_file)
    
    def get_clipboard_image_bytes(self) -> bytes:
        image = self.get_clipboard_image()
        return self.qimage_to_bytes(image)
    

    def write_text_to_clipboard(self, text: str):
        """
        将文本写入剪贴板
        """
        try:
            print(text)
            # 创建 QApplication 实例
            # 将文本写入剪贴板
            self.clipboard.setText(text, mode=QClipboard.Clipboard)
            # print("Text written to clipboard successfully")
            # 启动事件循环
        except Exception as e:
            print(f"Error writing text to clipboard: {e}")
            raise
        finally:
            # 退出应用程序
            self.app.quit()

    def process_clipboard_text(self, text: str):
        print("Writing text to clipboard...")
        try:# 创建 QApplication 实例
            QTimer.singleShot(0, lambda:self.write_text_to_clipboard(text))
            print("Text written to clipboard successfully.")
            # 启动事件循环
            self.app.exec_()
        except Exception as e:
            print(f"Error processing text: {e}")


if __name__ == "__main__":

    # 创建 ClipboardTool 实例
    getter = ClipboardTool()

    # 调用函数获取剪贴板图片
    # pil_image = getter.get_clipboard_image()

    # if pil_image:
    #     # 保存图片到文件
    #     pil_image.save('clipboard_image.png')
    #     print("图片已保存到 clipboard_image.png")
    # else:
    #     print("未能获取剪贴板中的图片") 
    getter.process_clipboard_text("hhhhhh")
