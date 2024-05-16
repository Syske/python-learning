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

def get_pages(url, base_url):
    results = []
    for page in range(4):
        page_url =f'{base_url}/jianlai/index{page + 1}.html'
        datas = get_page_info(url=page_url, base_url=base_url)
        if len(datas) > 0:
            results += datas
    return results
        
def get_page_info(url, base_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; MEIZU 18s Build/TKQ1.221114.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36"
    }
    response = requests.get(url=url, headers=headers, verify=False)
    response.encoding='gbk'
    # print(response.text)
    selector1 = parsel.Selector(response.text)
    datas = []
    contents = selector1.css('.chapter9 > div')
    for content in contents:
        href = base_url + content.css('a::attr(href)').get()
        title = content.css('a::text').get()
        datas.append((href, title))
    # print(next_page_list)
    # print(next_page_list[len(next_page_list) - 1].get())
    return datas
            
def get_single_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; MEIZU 18s Build/TKQ1.221114.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36"
    }
    response = requests.get(url=url, headers=headers, verify=False)
    response.encoding='gbk'
    # print(response.text)

    selector1 = parsel.Selector(response.text)
    contents = selector1.css('#content').get()
    print(contents)
    return contents
        
if __name__ == "__main__":
    # https://www.dajiadu8.com/32/32783/
    base_url = "https://www.1pwx.com"
    url = f"{base_url}/jianlai/index1.html"
    results = get_pages(url=url, base_url=base_url)
    print(results)
    path = './剑来'
    if not os.path.exists(path):
        os.mkdir(path)
    index = 1
    for result in results:
        with open(f'{path}/{index} {result[1]}.txt', 'w+', encoding='utf-8') as f:
            content = get_single_page(result[0])
            f.write(content)
        index += 1
    # get_single_page(1)
    # batch_load(559)