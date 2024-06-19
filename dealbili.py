# coding: utf-8
import requests
import parsel
import re
import urllib3
import time
import json
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()


def matchValue(reStr, sourceContent, matchIndex):
    pat = re.compile(reStr) #用()表示1个组，2个组
    m = pat.search(sourceContent)
    if m == None:
        return 
    return m.group(matchIndex) #默认为0，表示匹配整个字符串



def build_content(datas):
    content = ''
    for data in datas:
        content += f"### {data[0]} \n 视频在线地址：[在线地址]({data[1]}) \n ![]({data[2]}) \n"
    return content

def batch_load(total_page):
    file_name = "./hsck/hsck{}.md"
    
    count = 0
    file_content = ''
    for i in range(total_page):
        if i >= 0:
            file_content += build_content(get_single_page(pageNum=(i + 1)))
            print(f"第{i+1}页")
            if (i + 1) % 10 == 0 or total_page == i + 1:
                count += 1
                # print(file_content)
                with open(file_name.format(count), 'a+', encoding='utf-8') as f:
                    f.write(file_content)
                    file_content = ''
            time.sleep(0.5) 
            
def get_single_page(url, title):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; MEIZU 18s Build/TKQ1.221114.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36"
    }
    response = requests.get(url=f"{url}", headers=headers, verify=False)
    response.encoding='utf-8'
    selector1 = parsel.Selector(response.text)
    header_contents = selector1.css('.video script::text')
    for content in header_contents:
        contentStr = content.get()
        # print(contentStr)
        if 'var options' in contentStr:
            # print(contentStr)
            temp_data = matchValue('var options\s+\S+\s((.+));', contentStr, 1)
            
            # print(temp_data)
            json_data = json.loads(temp_data)
            video_url = json_data['readyVideoUrl']
            print(title, json_data['readyVideoUrl'])
            video_content = requests.get(url=video_url,headers=headers).content

            # 创建mp4文件，写入二进制数据
            with open (title+".mp4", mode = "wb") as f :
                f.write(video_content)
        
def get_page_info(url):
# url = f'http://367hsck.cc/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; MEIZU 18s Build/TKQ1.221114.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36"
    }
    response = requests.get(url=f"{url}", headers=headers, verify=False)
    response.encoding='utf-8'
    # print(response.text)
    open("test.html", mode='w', encoding='utf-8').write(response.text)
    # page_url = matchValue(r'strU=\s*"([^"]+)', response.text, 1)
    # print(page_url)
    # parsed_url = urlparse(url)
    # print(parsed_url)
    # print(parsed_url.path)
    # response = requests.get(url=page_url + parsed_url.path + "&p=/", headers=headers, verify=False)
    # print(response.text)
    # print(dir(response))

    selector1 = parsel.Selector(response.text)
    contents = selector1.css('body > script::text')
    title = selector1.css('title::text').get().replace('|', '')
    
    index = 1
    datas = []
    for content in contents:
        # content = contents[3]

        # print(content.get())
        pic_info = content
        contentStr = pic_info.get()
        
        if contentStr.startswith('window.__INITIAL_STATE__='):
            # temp_data = contentStr.replace('window.__INITIAL_STATE__=', '')
            
            temp_data = matchValue('window.__INITIAL_STATE__=((.+));\(fun', contentStr, 1)
            # print(temp_data)
            json_data = json.loads(temp_data)
            pages = json_data['video']['viewInfo']['pages']
            for page in pages:
                datas.append((page['page'], page['part']))
            # print(json_data['video']['viewInfo']['videos'])
            
            # open('test.json',mode='w+', encoding='utf-8').write(json.dumps(json_data['video'], ensure_ascii=False))
        # title_info = content.css(".stui-vodlist__detail > h4")
        # title = title_info.css("a::text")
        # href = title_info.css("a::attr(href)")
        # print(contentStr)
        # print(title.get())
        # print(url + href.get())
        # datas.append((title.get(), url + href.get(), pic_info.get()))
        index += 1
    return datas,title
        
if __name__ == "__main__":
    # 第三季
    #base_url = "https://www.bilibili.com/video/BV1uz421C7Ss"
    # 第一季
    # base_url = "https://www.bilibili.com/video/BV1mE42137KN"
    # 第二季
    # base_url = "https://www.bilibili.com/video/BV1qM4m1C7EB"
    base_url = "https://www.bilibili.com/video/BV1os421c7AE"
    # 第三季
    # url = f'{base_url}/?spm_id_from=333.999.0.0&vd_source=822695a88279c29d1d77cff2810689ad'
    # 第二季
    # url = f'{base_url}/?spm_id_from=333.1007.0.0&vd_source=822695a88279c29d1d77cff2810689ad'
    url = f'{base_url}/?spm_id_from=333.999.0.0&vd_source=822695a88279c29d1d77cff2810689ad'
    pages, title = get_page_info(url)
    if not os.path.exists(str(title)):
        os.mkdir(str(title))
    with ThreadPoolExecutor(max_workers=10) as threadPool:
        for i in tqdm(range(len(pages)), desc='video download Processing'):
            page = pages[i]
            threadPool.submit(get_single_page, f'{base_url}?p={page[0]}', f'{title}/{page[1]}')
            time.sleep(0.5)
    # batch_load(559)
    # get_single_page(url, '第一集')
