# coding: utf-8
import requests
import parsel
import re
import urllib3
import time
import json
import os
import uuid
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
                
                
def build_player_url(json_data):
    ts_url = "https://api.bilibili.com/x/click-interface/click/now"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; MEIZU 18s Build/TKQ1.221114.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36"
    }
    ts_response = requests.get(ts_url, headers=headers)
    ts_json = ts_response.json()
    wts = ts_json['data']['now']
    w_rid = str(uuid.uuid4()).replace('-', '')
    url =  f'''
            https://api.bilibili.com/x/player/wbi/playurl?avid={json_data['aid']}&bvid={json_data['bvid']}&cid={json_data['cid']}&qn=0&fnver=0&fnval=4048&fourk=1&gaia_source=external-link&from_client=BROWSER&is_main_page=false&need_fragment=false&isGaiaAvoided=true&session=160081202c9a2b89261bd261cb1a967c&voice_balance=1&web_location=1315873&w_rid={w_rid}&wts={wts}
            '''
    return url.replace('\n', '')
    
                
def get_single_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; MEIZU 18s Build/TKQ1.221114.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36"
    }
    response = requests.get(url=f"{url}", headers=headers, verify=False)
    response.encoding='utf-8'
    selector1 = parsel.Selector(response.text)
    open("test-player.html", mode='w', encoding='utf-8').write(response.text)
    
                
def get_player_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; MEIZU 18s Build/TKQ1.221114.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36"
    }
    response = requests.get(url=f"{url}", headers=headers, verify=False)
    response.encoding='utf-8'
    selector1 = parsel.Selector(response.text)
    contents = selector1.css('script[data-vue-meta="true"][type="application/ld+json"]::text')
    for content in contents:
        json_data = json.loads(content.get())
        if json_data['@type'] == 'VideoObject':
            print(json_data)
            return json_data['embedUrl']
    return None
        
def get_page_info(url):
# url = f'http://367hsck.cc/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; MEIZU 18s Build/TKQ1.221114.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36"
    }
    response = requests.get(url=f"{url}", headers=headers, verify=False)
    response.encoding='utf-8'
    # print(response.text)
    # open("test.html", mode='w', encoding='utf-8').write(response.text)
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
            # pages = json_data['video']['viewInfo']['pages']
            # print(json_data['video']['viewInfo'])
            # open("pages.json", mode='w', encoding='utf-8').write(json.dumps(json_data['video']['viewInfo']['ugc_season']['sections'], ensure_ascii=False))
            sections = json_data['video']['viewInfo']['ugc_season']['sections']
            for section in sections:
                # print(section['episodes'])
                for episode in section['episodes']:
                    player_url = build_player_url(episode)
                    response = requests.get(url=player_url, headers=headers)
                    videos = response.json()['data']['dash']['video']
                    # print(response.json()['data']['dash']['video'])
                    print("\n")
                    max_id = 0
                    video_url = None
                    title = episode['title']
                    for video in videos:
                        # print(video['id'])
                        if video['id'] > max_id:
                            # print(video)
                            video_url = video['baseUrl']
                            max_id = video['id']
                    print(title, max_id, video_url)
                    time.sleep(0.5) 
                    # print(title, json_data['readyVideoUrl'])
                    video_content = requests.get(url=video_url,headers=headers).content
                    time.sleep(0.5) 
                    # 创建mp4文件，写入二进制数据
                    with open (title+".m4s", mode = "wb") as f :
                        f.write(video_content)
            # for page in pages:
            #     datas.append((page['page'], page['part']))
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
    base_url = "https://www.bilibili.com/video/BV18NhTerEo3"
    # 第三季
    # url = f'{base_url}/?spm_id_from=333.999.0.0&vd_source=822695a88279c29d1d77cff2810689ad'
    # 第二季
    # url = f'{base_url}/?spm_id_from=333.1007.0.0&vd_source=822695a88279c29d1d77cff2810689ad'
    url = f'{base_url}/?spm_id_from=333.880.my_history.page.click&vd_source=822695a88279c29d1d77cff2810689ad'
    # next_url = get_player_info(url=url)
    # get_single_page(next_url)
    pages, title = get_page_info(url)
    # if not os.path.exists(str(title)):
    #     os.mkdir(str(title))
    # with ThreadPoolExecutor(max_workers=10) as threadPool:
    #     for i in tqdm(range(len(pages)), desc='video download Processing'):
    #         page = pages[i]
    #         threadPool.submit(get_single_page, f'{base_url}?p={page[0]}', f'{title}/{page[1]}')
    #         time.sleep(0.5)
    # batch_load(559)
    # get_single_page(url, '第一集')
