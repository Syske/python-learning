# -*- coding: utf-8 -*-

import oss2
from PIL import Image
import io
import uuid
from pydantic import BaseModel
import win32clipboard as clip
from config import Settings


class AliyunPicUploader(BaseModel):
    bucket_name: str
    endpoint: str
    access_key: str
    secret_key: str
    region: str
    path: str
    
    def __init__(self, **data):
        super().__init__(**data)
        # 执行额外的初始化逻辑

    def upload2aliyunoss(self, img_data: bytes):
        """
        上传图片到阿里云oss
        """
        # 使用获取的RAM用户的访问密钥配置访问凭证
        auth = oss2.AuthV4(self.access_key, self.secret_key)

        filename = f"{uuid.uuid4()}.jpg"

        # 填写Bucket名称。
        bucket = oss2.Bucket(auth, endpoint=self.endpoint, bucket_name=self.bucket_name, region=self.region)

        # 填写Object完整路径和Bytes内容。Object完整路径中不能包含Bucket名称。
        result = bucket.put_object(f'{self.path}/{filename}', img_data)
        print(result.status)
        print(result.resp)
        print(result.etag)
        print(result.crc)
        if result.status == 200:
            remote_file = f'https://{self.bucket_name}.oss-{self.region}.aliyuncs.com/{self.path}/{filename}'
            print(remote_file)
            return remote_file
        else:
            return None
    
    def clipboard_img_upload_aliyun(self):
        """
        上传剪贴板图片到阿里云
        """
        # 读取剪贴板图片
        clipboard_img = self.read_clipboard_img()
        print(clipboard_img)
        if clipboard_img != None:
            img_bytes = self.image2bytes(clipboard_img)
            pic_url = self.upload2aliyunoss(img_bytes)
            if pic_url != None:
                return pic_url
        return None

    def read_clipboard_img(self) -> Image.Image:
        """
        读取剪贴板图片
        """
        # 获取剪贴板的数据（假设为图片）
        clip.OpenClipboard()
        try:
            if clip.IsClipboardFormatAvailable(clip.CF_DIB):
                dib = clip.GetClipboardData(clip.CF_DIB)
                img = Image.open(io.BytesIO(dib))
                return img
            else:
            
                return None
        except Exception as e:
            print(e)
            return None
        finally:
            clip.CloseClipboard()

    def set_text_to_clipboard(self, text):
        """
        将内容写入剪贴板
        """
        clip.OpenClipboard()
        clip.EmptyClipboard()
        clip.SetClipboardText(text)
        clip.CloseClipboard()

    def image2bytes(self, image: Image.Image) -> bytes:
        """
        图片转bytes
        """
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="JPEG")
        return image_bytes.getvalue()
    
    def img_url_format(self, pic_url, type="md"):
        if pic_url == None:
            return None
        if type == "md":
            return f"![]({pic_url})"
        return pic_url
        


if __name__ == "__main__":
    config = Settings()
    print(config.uploader_config)
    uploader = AliyunPicUploader(
        **config.uploader_config
    )
    print(config, uploader)
    pic_url = uploader.clipboard_img_upload_aliyun()
    pic_url_format = uploader.img_url_format(pic_url=pic_url)
    if pic_url_format != None:
        uploader.set_text_to_clipboard(pic_url_format)