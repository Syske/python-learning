import requests
import parsel
import re
import urllib3
import time
from urllib.parse import urlparse
import os

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
    file_priex = "pwxxx"
    file_dir = f"./{file_priex}/{file_priex}"
    file_name = "{}.md"
    
    if not os.path.exists(file_priex):
        os.mkdir(file_priex)
    
    count = 0
    file_content = ''
    for i in range(total_page):
        if i >= 0:
            file_content += build_content(get_single_page(pageNum=(i + 1)))
            print(f"第{i+1}页")
            if (i + 1) % 10 == 0 or total_page == i + 1:
                count += 1
                # print(file_content)
                with open(file_name.format(file_dir, count), 'a+', encoding='utf-8') as f:
                    f.write(file_content)
                    file_content = ''
            time.sleep(0.5) 
        
def get_single_page(pageNum):
    base_url = f'https://.fun'

    url = f'{base_url}/pwxxx/vod/type/id/1/page/{pageNum}.html'
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; MEIZU 18s Build/TKQ1.221114.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36"
    }
    # response = requests.get(url=f"{url}vodtype/2-{pageNum}.html", headers=headers, verify=False)
    response = requests.get(url=f"{url}", headers=headers, verify=False)
    response.encoding="utf-8"
    # print(response.text)
    # page_url = matchValue(r'strU=\s*"([^"]+)', response.text, 1)
    # print(page_url)
    # parsed_url = urlparse(url)
    # print(parsed_url)
    # print(parsed_url.path)
    # response = requests.get(url=page_url + parsed_url.path + "&p=/", headers=headers, verify=False)
    # print(response.text)
    # print(dir(response))

    selector1 = parsel.Selector(response.text)
    contents = selector1.css('.stui-vodlist')
    # print(contents[0].get())
    index = 1
    datas = []
    
    for content in contents:
        # content = contents[3]
        # print(content.get())
        # if index > 2:
            # print(content.get())
        href = base_url + content.css('li > .stui-vodlist__box > a::attr(href)').get()
        print(href)
        # img_url = content.css('li > stui-vodlist__box > a > img::attr(src)').get()
        img_url = content.css('li > .stui-vodlist__box > a::attr(data-original)').get()
        # img_url = matchValue(r"url\((.+)\)", img_url, 1)
        print(img_url)
        title = content.css('li > .stui-vodlist__box > a::attr(title)').get()
        print(title)
        if title != None:
            datas.append((title, href, img_url))
        index += 1
    return datas
        
if __name__ == "__main__":
    # get_single_page(1)
    batch_load(3009)