import os
import re

path = 'D:/workspace/learning/learning-dome-code'

file = open(path + '/README.md', mode='r', encoding='utf-8')
file_content = file.read();
print(f'file_content:{file_content}')
dirs = os.listdir(path)

unknow_folder=''
for d in dirs:
    result = file_content.find(d)
    print(f'dir:{d},result:{result}')
    if (result == -1):
         unknow_folder += f'[{d}](./{d}):'
print(unknow_folder)