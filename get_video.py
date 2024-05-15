
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

def getVideoList(indexUrl):
    vodUrl = getVideoM3u8Url(indexUrl)
    # requests.get(url, headers).text
    return getTsFileUrlList(vodUrl)

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

def getTsFileUrl(pageUrl):
    response = requests.get(url=pageUrl, headers=headers)
    response.encoding="utf-8"
    # print(response.text)
    selector1 = parsel.Selector(response.text)
    content = selector1.css('.embed-responsive > script::text').get()
    # print(content)
    matchStr = matchValue(r'var player_aaaa=(.*)', content, 1)
    
    json_data = json.loads(matchStr)
    return (json_data['url'], json_data['url_next'])

def getTsFileUrlList(m3u8Url, baseUrl=None):
    fileExt = r"/(\w+.m3u8)"        
    valueStr = matchValue(reStr=fileExt, sourceContent=m3u8Url, matchIndex=1)
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
            threadPool.submit(downloadOneFile, url, fileSavePath, index, total)
            time.sleep(0.1)
        threadPool.shutdown()
        #fileMerge(fileSavePath)    
    print('下载完成', fileSavePath)
    
def downloadOneFile(url, fileSavePath, index, total):
    try:
        downloadFile(url, fileSavePath, index, total)
    except Exception as e:
        print("downloadOneFile error, will retury", e, index)
        downloadFile(url, fileSavePath, index, total)

def downloadFile(url, fileSavePath, index, total):
    ts_video = requests.get(url = url, headers=headers)
    with open('{}/{}.ts'.format(fileSavePath, str(index)), 'wb') as file:
        context = ts_video.content
        file.write(context)
        # print(f'正在写入第{total}/{index + 1}个文件')

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
    
def matchValue(reStr, sourceContent, matchIndex):
    pat = re.compile(reStr) #用()表示1个组，2个组
    m = pat.search(sourceContent)
    if m == None:
        return 
    return m.group(matchIndex) #默认为0，表示匹配整个字符串
    
if __name__ == "__main__":
    indexUrl = "https://www.tianxinjzjg.com/vodplay/59844-1-1.html"
    urlList = getVideoM3u8Url(indexUrl)
    print(urlList)
    data = getTsFileUrl(urlList[0])
    print(data)