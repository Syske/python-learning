import requests
import os
from concurrent.futures import ThreadPoolExecutor
import re
import time
from Crypto.Cipher import AES   # 用于AES解码

headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }

class VideoToool:
    

    @staticmethod
    def getTsFileUrlInfo(m3u8Url, baseUrl=None):
        fileExt = r"/(\w+.m3u8)"        
        valueStr = VideoToool.matchValue(reStr=fileExt, sourceContent=m3u8Url, matchIndex=1)
        print(valueStr)
        if baseUrl == None:
            baseUrl = m3u8Url[:-len(valueStr)]
        print(fileExt)
        reponse = requests.get(url = m3u8Url, headers=headers)
        ts_rs = reponse.text
        print("ts_rs:", ts_rs)
        list_content = ts_rs.split('\n')
        # print('list_content:{}'.format(list_content))
        player_list = []
        ext_key = None
        for line in list_content:
            # print(line)
        # 以下拼接方式可能会根据自己的需求进行改动
            if '#EXT-X-KEY' in line:
                ext_key = line.split('URI=')[1].replace("\"", '')
            if '#EXTINF' in line:
                continue
            else:
                if line.find("http") != -1:
                    player_list.append(f'{line}')
                else:                
                    player_list.append(f'{baseUrl}/{line}')
        print('数据列表组装完成-size: {}'.format(len(player_list)))
        return player_list,ext_key

    @staticmethod
    def fileDownloadWithdecrypt(fileSavePath, player_list, key, baseUrl=None, deleteSpiltStart=None, deleteSpiltEnd=None):
        
        # print(player_list)
        if not os.path.exists(fileSavePath):
            os.mkdir(fileSavePath)
        if deleteSpiltStart != None and deleteSpiltEnd != None:
            print(player_list[deleteSpiltStart-1:deleteSpiltStart-1])
            del player_list[164:169]
        total = len(player_list)
        
        with ThreadPoolExecutor(max_workers=20) as threadPool:
            for index, url in enumerate(player_list):
                if baseUrl != None:
                    url = f'{baseUrl}/{url}'
                threadPool.submit(VideoToool.downloadOneFile, url, fileSavePath, index, total, key)
                time.sleep(0.1)
            threadPool.shutdown()
            #fileMerge(fileSavePath)    
        print('下载完成', fileSavePath)
        
    @staticmethod    
    def downloadOneFile(url, fileSavePath, index, total, key):
        try:
            VideoToool.downloadFile(url, fileSavePath, index, total, key)
        except Exception as e:
            print("downloadOneFile error, will retury", e, index)
            VideoToool.downloadFile(url, fileSavePath, index, total, key)

    @staticmethod
    def downloadFile(url, fileSavePath, index, total, key):
        url_ext_index = url.rfind('.')
        file_ext = url[url_ext_index:]
        ts_video = requests.get(url = url, headers=headers)
        with open('{}/{}{}'.format(fileSavePath, str(index)), str(file_ext), 'wb') as file:
            context = ts_video.content
            context = VideoToool.decrypt(ts_video.content, key)
            file.write(context)
            # print(f'正在写入第{total}/{index + 1}个文件')
            
    @staticmethod
    def fileMerge(filePath, deleteSpiltStart=None, deleteSpiltEnd=None):
        c = os.listdir(filePath)
        with open('%s.mp4' % filePath, 'wb+') as f:
            for i in range(len(c)):
                if deleteSpiltEnd != None and deleteSpiltStart != None and i >= deleteSpiltStart -1  and i <= deleteSpiltEnd - 1:
                    print("ad file",  str(i))
                else:
                    x = open('{}/{}.ts'.format(filePath, str(i)), 'rb').read()
                    f.write(x)
        # shutil.rmtree(filePath)
        print('合并完成')
    
    @staticmethod   
    def matchValue(reStr, sourceContent, matchIndex):
        pat = re.compile(reStr) #用()表示1个组，2个组
        m = pat.search(sourceContent)
        if m == None:
            return 
        return m.group(matchIndex) #默认为0，表示匹配整个字符串
    
    @staticmethod
    def decrypt(context, key=None):
        cryptor = AES.new(key, AES.MODE_CBC)
        decrypt_content = cryptor.decrypt(context)
        return decrypt_content