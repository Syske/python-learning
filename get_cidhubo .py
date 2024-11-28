import requests
import parsel
import re
import time
import json
import m3u8
from concurrent.futures import ThreadPoolExecutor,as_completed
from get_video import GetVideo
import os

def get_single_page(pageNum):
    url = f"https://www.cupfox8.cc/foxplay/34546-1-{pageNum}.html"
    print(url)
    response = requests.get(url=url)
    selector1 = parsel.Selector(response.text)
    contents = selector1.css('body > div.page.player > div.main > div > div.module.module-player > div > div.player-box > div > script:nth-child(1)::text')
    # print(contents.get())
    # print(baseUrl + picUrl)
    # print(video_url)
    values = matchValue("var player_aaaa=((.+))", contents.get(), 1)
    datas = json.loads(values)
    print(datas)

    return datas

def build_content(datas):
    content = ''
    for data in datas:
        content += f"### {data[0]} \n 视频在线地址：[在线地址]({data[1]}) \n ![]({data[2]}) \n 播放地址：{data[3]}\n"
    return content

def batch_load(total_page):
    file_name = "./titiwo/titiwo{}.md"
    
    count = 5
    file_content = ''
    for i in range(total_page):
        if i > 200:
            file_content += build_content(get_single_page(pageNum=(i + 1)))
            print(f"第{i+1}页")
            if (i + 1) % 50 == 0 or total_page == i + 1:
                count += 1
                print(file_content)
                with open(file_name.format(count), 'a+', encoding='utf-8') as f:
                    f.write(file_content)
                    file_content = ''
            time.sleep(0.5) 
            
def batch_load_for_zhifou(total_page):
    datas = list()
    for i in range(total_page):
        vod_json = get_single_page(pageNum=(i + 1))
        datas.append((vod_json['link_next'], vod_json['url'], vod_json['url_next']))
        time.sleep(0.5) 
    return datas
        
    
def matchValue(reStr, sourceContent, matchIndex):
    pat = re.compile(reStr) #用()表示1个组，2个组
    m = pat.search(sourceContent)
    if m == None:
        return 
    return m.group(matchIndex) #默认为0，表示匹配整个字符串

def getTsFileInfo(url):
    response = requests.get(url=url)
    print(response.text)
    
def bach_download(base_dir):
    content = open("zhifou_m3u8.json", encoding="utf-8").read()
    json_data = json.loads(content)
    for i, data in enumerate(json_data):
        if i > 0:
            m3u8_url = get_m3u8_url(data[1])
            print(m3u8_url)
            download(m3u8_url, base_dir=base_dir, index=f'{i + 1}')
    
    
def download(m3u8_url, base_dir, index):
    m3u8_obj = m3u8.load(m3u8_url)
    total = len(m3u8_obj.segments)
    fileSavePath = f'{base_dir}/第{index}集'
    if not os.path.exists(fileSavePath):
        os.makedirs(fileSavePath)
    with ThreadPoolExecutor(max_workers=20) as threadPool:
        futures = []
        for i, segment in enumerate(m3u8_obj.segments):
            segment_url = segment.absolute_uri
            futures.append(threadPool.submit(GetVideo.downloadOneFile, segment_url, fileSavePath, i, total))
          

        # 等待所有任务完成
        for future in as_completed(futures):
            try:
                future.result()  # 获取结果并捕获异常
            except Exception as e:
                print(f"Task failed with exception: {e}")

def batch_merge_file(filePath):
    file_list = os.listdir(filePath)
    print(file_list)
    for f in file_list:
        GetVideo.fileMerge(filePath=f'{filePath}/{f}', exculd_index=[194, 195, 196, 197, 198, 499,500, 501, 502, 503])
                
def get_m3u8_url(index_url):
    return index_url.replace('index', '1000k/hls/mixed')

def merge_mp4(filePath):
    file_list = os.listdir(filePath)
    filePath = filePath.replace('\\', '/')
    with open('%s.txt' % filePath, 'w+', encoding='utf-8') as f:
        content = ''
        for file in file_list:
            content += f"file '{filePath}/{file}'\n"
        f.write(content)
    
    
if __name__ == "__main__":
    # get_single_page(1)
    # datas = batch_load_for_zhifou(73)
    # datas_json = json.dumps(datas)
    # print(datas_json)
    # open("zhifou_m3u8.json", mode="w+", encoding="utf-8").write(datas_json)
    url = "https://vip1.lz-cdn.com/20220606/17432_0982c867/index.m3u8"
    # getTsFileInfo(url)
    url = "https://vip1.lz-cdn.com/20220606/17432_0982c867/1000k/hls/mixed.m3u8"
    # getTsFileInfo(url)
    base_dir = "./知否知否，应是红肥绿瘦"
    # m3u8_obj = m3u8.load(url)
    # total = len(m3u8_obj.segments)
    
    # download_and_merge(url, fileSavePath=fileSavePath)
    # bach_download(base_dir)
    # batch_merge_file(base_dir)
    merge_mp4("D:\\workspace\\learning\\python-learning\\知否知否，应是红肥绿瘦\\第1集")