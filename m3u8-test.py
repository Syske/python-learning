import m3u8
import requests

url = "https://vip1.lz-cdn.com/20220606/17432_0982c867/1000k/hls/mixed.m3u8"
m3u8_obj = m3u8.load(url)
print(dir(m3u8_obj))

# 下载每一个片段并保存到本地
for i, segment in enumerate(m3u8_obj.segments):
    segment_url = segment.absolute_uri
    print(segment_url)
    # response = requests.get(segment_url)
    