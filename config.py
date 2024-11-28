import yaml
from pathlib import Path
from typing import Dict

import os
from pathlib import Path

home = os.path.expanduser('~')
HOME = Path(home)
BASE_DIR = HOME.joinpath('.py-config')
if not BASE_DIR.exists():
    BASE_DIR.mkdir(parents=True)

__all__ = ["BASE_DIR"]


template = '''
# 可用图床
pic-uploader: 
  aliyun:
    config:
      endpoint: http://oss-cn-hangzhou.aliyuncs.com
      bucket_name: aaa
      access_key: aaa
      secret_key:  aaa
      region: cn-hangzhou
      path: imgs
'''


class Settings:
    CONFIG_DIR: Path = BASE_DIR
    config: Dict
    uploader_config: Dict

    def __init__(self):
        self.__init_env()
        self.load_config()
        
    def __init_env(self):
        if not self.CONFIG_DIR.exists():
            Path.mkdir(self.CONFIG_DIR)
            
        path = self.CONFIG_DIR.joinpath('config.yaml')
        print(f"config file path in : {path}")
        if not path.exists():
            print(f"init config in {path}, you should replace config to yours")
            with path.open(mode='w', encoding='utf-8') as f:
                f.write(template)

    def load_config(self):
        config_file = self.CONFIG_DIR.joinpath('config.yaml')
        with open(config_file.resolve(), 'r', encoding='utf-8') as f:
            config = yaml.load(f.read(), Loader=yaml.CFullLoader)
            self.load_pic_uploader_config(config)
    
    # pic uploader配置
    def load_pic_uploader_config(self, config):
        try:
            print(config)
            pic_uploader = config.get('pic-uploader', dict())
            self.uploader_config = pic_uploader['aliyun']['config']
        except ImportError:
            msg = f'load_pic_uploader_config error,{pic_uploader}'
            print(msg)