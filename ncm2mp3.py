import os
from ncmdump import NeteaseCloudMusicFile

# 获取所有需要转换的音乐文件
directory = "D:\\CloudMusic\\VipSongsDownload\\"
output_directory = "./output_music/"
files_names = os.listdir(directory)
if not os.path.exists(output_directory):
    os.mkdir(output_directory)
# 输出转换后的文件
for name in files_names:
    if not name.endswith(".ncm"):
        continue
    input_music = directory + name
    ncmfile = NeteaseCloudMusicFile(input_music)
    ncmfile.decrypt()
    print(ncmfile.music_metadata)  # 显示音乐元数据
    ncmfile.dump_music(output_directory + name.replace('.ncm', '.mp3'))  # 自动检测正确的后缀并转换
