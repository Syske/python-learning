import struct
import base64
import requests
import random
import time

headers = {
    't': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjQ0MTUzMzUsIm5iZiI6MTY2NDE1NzkzNSwiaWF0IjoxNjY0MTU2MTM1LCJqdGkiOiJDTTpjYXRfbWF0Y2g6bHQxMjM0NTYiLCJ1aWQiOjEyMjk0NjY1OCwidmVyIjoiMSIsImV4dCI6IjM2MzMzMjYyNjM2NTM2NjM2NjY1NjIzNDMzMzEzNjY2NjUzNDY0NjU2NjMyMzU2MiIsImNvZGUiOiJhNjNiNDZiNWE0ODdjODdlZWU5NWJjZGRkZWQ0YzQzZCIsImVuZCI6MTY2NDQxNTMzNTcwNX0.9F5rBan5yZ9q0pRnYJjK0NxqfW9Rg6mRMC4-iHUYujs',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.4.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF',
    'Referer': 'https://servicewechat.com/wx141bfb9b73c970a9/23/page-frame.html'

}
url = 'https://cat-match.easygame2021.com/sheep/v1/game/personal_info?'
r = requests.get(url, headers=headers)
print(f'=============================map_info_ex:\n{r.json()}\n===============================')
url = 'https://cat-match.easygame2021.com/sheep/v1/game/map_info_ex?matchType=3'
r = requests.get(url, headers=headers)
print(r.json())
map_md5 = r.json()['data']['map_md5'][1]
url = f'https://cat-match-static.easygame2021.com/maps/{map_md5}.txt'  # 由于每天获取的地图不一样，需要计算地图大小
r = requests.get(url)
print(f'============================maps:\n{r.json()}\n===============================')
levelData = r.json()['levelData']
p = []
for h in range(len(sum(levelData.values(), []))):  # 生成操作序列
    p.append({'chessIndex': 127 if h > 127 else h, 'timeTag': 127 if h > 127 else h})
GAME_DAILY = 0
GAME_TOPIC = 0
data = struct.pack('BB', 8, GAME_DAILY)
print(f'===========================p：\n{p}\n===============================')
for i in p:
    c, t = i.values()
    data += struct.pack('BBBBBB', 34, 4, 8, c, 16, t)
MatchPlayInfo = base64.b64encode(data)
print(f"============================MatchPlayInfo:\n{MatchPlayInfo.decode('utf-8')}")

cost_time = random.randint(1, 3600)
interval_time = random.randint(60, 300)
print(f'===========================休眠时间：\n{interval_time}\n===============================')
time.sleep(interval_time)
url = 'https://cat-match.easygame2021.com/sheep/v1/game/game_over_ex?'
r = requests.post(url, headers=headers,
                  json={'rank_score': 1, 'rank_state': 1, 'rank_time': cost_time, 'rank_role': 1, 'skin': 34,
                        'MatchPlayInfo': MatchPlayInfo.decode('utf-8')})

url = 'https://cat-match.easygame2021.com/sheep/v1/game/update_user_skin?skin=27'
r = requests.get(url, headers=headers)
print(f'===========================update_user_skin:\n{r.json()}\n===============================')
url = 'https://cat-match.easygame2021.com/sheep/v1/game/personal_info?'
r = requests.get(url, headers=headers)
print(f'===========================personal_info:\m{r.json()}\n===============================')



def multi_byte_int(number: int):
    # <128      : 1
    # <16384    : 2
    # <2097152  : 3
    # <268435456: 4
    # else      : 5
    if number < 128:
        return struct.pack('B', number)
    elif number < 16384:
        return struct.pack('BB', number & 127 | 128, number >> 7)
    elif number < 2097152:
        return struct.pack('BBB', number & 127 | 128, number >> 7 & 127 | 128, number >> 14)
    elif number < 268435456:
        return struct.pack('BBBB', number & 127 | 128, number >> 7 & 127 | 128, number >> 14 & 127 | 128, number >> 21)
    else:
        return struct.pack('BBBBB', number & 127 | 128, number >> 7 & 127 | 128, number >> 14 & 127 | 128, number >> 21 & 127 | 128, number >> 28)