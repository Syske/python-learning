
import requests
import re
import json
import parsel
import os
from concurrent.futures import ThreadPoolExecutor
import base64
import shutil
import time
import subprocess
import glob

headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

class GetVideo:
    
    @staticmethod
    def getVideoList(indexUrl):
        vodUrl = GetVideo.getVideoM3u8Url(indexUrl)
        # requests.get(url, headers).text
        return GetVideo.getTsFileUrlList(vodUrl)

    @staticmethod
    def getVideoM3u8Url(indexUrl):
        baseUrl = "https://www.tianxinjzjg.com"
        print("indextUrl:", indexUrl)    
        response = requests.get(url=indexUrl, headers=headers)
        response.encoding="utf-8"
        # print(response.text)
        selector1 = parsel.Selector(response.text)
        contents = selector1.css('#player1 > .myui-content__list > li')
        urlList = []
        for content in contents:
            href = content.css("a::attr(href)").get()
            urlList.append(baseUrl + href)
        
        return urlList

    @staticmethod
    def getTsFileUrl(pageUrl):
        response = requests.get(url=pageUrl, headers=headers)
        response.encoding="utf-8"
        # print(response.text)
        selector1 = parsel.Selector(response.text)
        content = selector1.css('.embed-responsive > script::text').get()
        # print(content)
        matchStr = GetVideo.matchValue(r'var player_aaaa=(.*)', content, 1)
        
        json_data = json.loads(matchStr)
        return (json_data['url'], json_data['url_next'])

    @staticmethod
    def getTsFileUrlList(m3u8Url, baseUrl=None):
        fileExt = r"/(\w+.m3u8)"        
        valueStr = GetVideo.matchValue(reStr=fileExt, sourceContent=m3u8Url, matchIndex=1)
        print(valueStr)
        if baseUrl == None:
            baseUrl = m3u8Url[:-len(valueStr)]
        if m3u8Url.find('v10.dious.cc') != -1:
            baseUrl = "https://v10.dious.cc"
        print(fileExt)
        reponse = requests.get(url = m3u8Url, headers=headers)
        ts_rs = reponse.text
        print(ts_rs)
        list_content = ts_rs.split('\n')
        # print('list_content:{}'.format(list_content))
        player_list = []
        
        for line in list_content:
            # print(line)
        # 以下拼接方式可能会根据自己的需求进行改动
            if '#EXTINF' in line:
                continue
            elif line.endswith('.ts'):
                if line.find("http") != -1:
                    player_list.append(f'{line}')
                else:                
                    player_list.append(f'{baseUrl}/{line}')
        print('数据列表组装完成-size: {}'.format(len(player_list)))
        return player_list

    @staticmethod
    def fileDownloadWithdecrypt(fileSavePath, player_list, baseUrl=None, deleteSpiltStart=None, deleteSpiltEnd=None):
        
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
                threadPool.submit(GetVideo.downloadOneFile, url, fileSavePath, index, total)
                time.sleep(0.1)
            threadPool.shutdown()
            #fileMerge(fileSavePath)    
        print('下载完成', fileSavePath)
        
    @staticmethod
    def downloadOneFile(url, fileSavePath, index, total, max_retries=3):
        retries = 0
        while retries < max_retries:
            try:
                GetVideo.downloadFile(url, fileSavePath, index, total)
                break
            except Exception as e:
                print(f"downloadOneFile error, retrying ({retries + 1}/{max_retries}): {e}, index: {index}")
                retries += 1
                time.sleep(1)  # 适当延迟重试

    @staticmethod
    def downloadFile(url, fileSavePath, index, total, timeout=10):
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # 检查请求是否成功
        with open(f'{fileSavePath}/{index}.ts', 'wb') as file:
            file.write(response.content)
            print(f'正在写入{fileSavePath}第{total}/{index + 1}个文件')

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
    def fileMerge(filePath, exculd_index:list):
        c = os.listdir(filePath)
        with open('%s.mp4' % filePath, 'wb+') as f:
            for i in range(len(c)):
                if i in exculd_index:
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
    
if __name__ == "__main__":
    indexUrl = "https://www.tianxinjzjg.com/vodplay/59844-1-1.html"
    urlList = GetVideo.getVideoM3u8Url(indexUrl)
    print(urlList)
    data = GetVideo.getTsFileUrl(urlList[0])
    print(data)