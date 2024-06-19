# coding: utf-8
import requests
import parsel
import urllib3

urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()

def get_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; MEIZU 18s Build/TKQ1.221114.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Mobile Safari/537.36"
    }
    response = requests.get(url=f"{url}", headers=headers, verify=False)
    response.encoding='utf-8'
    print(response.text)
    selector1 = parsel.Selector(response.text)
    header_contents = selector1.css('.desc-box')
    print(header_contents)
    
if __name__ == "__main__":
    url = "https://blog.csdn.net/banxia_frontend/article/details/134750300"
    get_info(url)