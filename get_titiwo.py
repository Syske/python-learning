import requests
import parsel
import re
import time

def get_single_page(pageNum):
    baseUrl = "https://titiwo.159i1.info"
    url = f"{baseUrl}/video/p{pageNum}.html"
    response = requests.get(url=url)
    selector1 = parsel.Selector(response.text)
    contents = selector1.css('#content >.post')
    datas = []
    for content in contents:
        # print(content.get())
        title = content.css(".info > h2 > a::text").get()
        href = content.css(".info > h2 > a::attr(href)").get()
        # print(title)
        # print(baseUrl + href)
        scriptContent = content.css("script::text").get()
        # print(scriptContent)
        picUrl = matchValue(r"pic:\s*'([^']+)'", scriptContent, 1)
        video_url = matchValue(r"url:\s*'([^']+)'", scriptContent, 1)
        datas.append((title, baseUrl + href, baseUrl + picUrl, video_url))
    # print(baseUrl + picUrl)
    # print(video_url)
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
        
    
def matchValue(reStr, sourceContent, matchIndex):
    pat = re.compile(reStr) #用()表示1个组，2个组
    m = pat.search(sourceContent)
    if m == None:
        return 
    return m.group(matchIndex) #默认为0，表示匹配整个字符串

if __name__ == "__main__":
    # get_single_page(1)
    batch_load(7838)