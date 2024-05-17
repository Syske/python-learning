
import requests
import parsel
import re
import urllib3
import time
import json
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
    file_dir = "./f52gg"
    file_name = "{}/f52gg{}.md"
    
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    
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

def get_page_info(url, base_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; MEIZU 18s Build/TKQ1.221114.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36"
    }
    # response = requests.get(url=f"{url}vodtype/2-{pageNum}.html", headers=headers, verify=False)
    response = requests.get(url=f"{url}", headers=headers, verify=False)
    response.encoding="utf-8"
    selector1 = parsel.Selector(response.text)
    contents = selector1.css('.myui-panel-box .tab-pane > ul')
    # body > div.container > div > div.col-lg-wide-75.col-md-wide-7.col-xs-1.padding-0 > div:nth-child(2) > div > div:nth-child(2) > div.myui-content__detail > h1
    page_title = selector1.css('.myui-content__detail h1::text').get()
    # print(contents[0].get())
    url_datas = []
    for content in contents:
        datas = []
        lists = content.css("li > a")
        for li in lists:
            href = ''
            if base_url != None:
                href = base_url + li.css('a::attr(href)').get()
            else:
                href = li.css('a::attr(href)').get()
            title = li.css("a::text").get()
            datas.append((title, href))
        url_datas.append(datas)
    return url_datas, page_title
            
def get_single_page(page_url):
    url = page_url
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
    # open('test.html', mode='w+', encoding='utf-8').write(response.text)
    # print(dir(response))

    selector1 = parsel.Selector(response.text)
    contents = selector1.css('.embed-responsive > script::text')
    # print(contents[0].get())
    temp_data = matchValue('var player_aaaa=((.+))', contents[0].get(), 1)
    # print(temp_data)
    json_data = json.loads(temp_data)
    url = json_data['url']
    url_nex = json_data['url_next']
    print(url)
    print(url_nex)

    return url, url_nex
        
if __name__ == "__main__":
    base_url = "https://m.iuys.cc"
    url = f'{base_url}/voddetail/4184.html'
    url_datas,title = get_page_info(url=url, base_url=base_url)
    # print(url_datas, title)
    get_single_page(url_datas[0][0][1])
    # batch_load(342)