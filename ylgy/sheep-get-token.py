
import base64
import random
import sys
import time

import requests
import urllib3

# 获取用户信息接口
get_user_info_api = "https://cat-match.easygame2021.com/sheep/v1/game/user_info?uid=%s&t=%s"
# 用户登录接口，POST请求 需要wx_open_id
user_login_api = "https://cat-match.easygame2021.com/sheep/sheep/v1/user/login_wx"

#uid=68710973
uid=43377270
sacrifice_t_encryption = "ZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmxlSEFpT2pFMk9UUTFNelF4TXpjc0ltNWlaaUk2TVRZMk16UXpNVGt6Tnl3aWFXRjBJam94TmpZek5ETXdNVE0zTENKcWRHa2lPaUpEVFRwallYUmZiV0YwWTJnNmJIUXhNak0wTlRZaUxDSnZjR1Z1WDJsa0lqb2lJaXdpZFdsa0lqb3hNelU1TmprMU1pd2laR1ZpZFdjaU9pSWlMQ0pzWVc1bklqb2lJbjAucnhOcDY5Q3lfVW1ZWnQxdXpzR2tJS0ZCT1plaFczdlh6bzNrbHRKdHliWQ=="
#sacrifice_t = base64.b64decode(sacrifice_t_encryption.encode("utf-8")).decode("utf-8")
sacrifice_t = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQ2NTg5NzEsIm5iZiI6MTY2MzU1Njc3MSwiaWF0IjoxNjYzNTU0OTcxLCJqdGkiOiJDTTpjYXRfbWF0Y2g6bHQxMjM0NTYiLCJvcGVuX2lkIjoiIiwidWlkIjo2ODcxMDk3MywiZGVidWciOiIiLCJsYW5nIjoiIn0.Sr-cMe5aK9Gy9aBN6dMwuR2ZoOf22OyJgrnSrWRX2FQ"
header_user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.27(0x18001b36) NetType/WIFI Language/zh_CN"

urllib3.disable_warnings()
request_header = {
    "Host": "cat-match.easygame2021.com",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.27(0x18001b36) NetType/WIFI Language/zh_CN",
    "Referer": "https://servicewechat.com/wx141bfb9b73c970a9/17/page-frame.html",
    "Accept-Encoding": "gzip,compress,br,deflate",
    "Connection": "close"
}

print("sacrifice_t:{}".format(sacrifice_t))
get_res = requests.get(get_user_info_api % (uid, sacrifice_t), headers=request_header, timeout=15, verify=False)
if get_res.status_code == 200:
    print("返回结果content：{}".format(get_res.content))
    result_json = get_res.json()
    print("返回结果：{}".format(result_json))
    wxOpenId = result_json["data"]["wx_open_id"]
    print("wxOpenId：{}".format(wxOpenId))
    #avatar = result_json["data"]["avatar"]
    avatar = "0"
    print("avatar：{}".format(avatar))
else:
    print("请求失败")
    print("请求状态：{}".format(get_res.status_code))
    sys.exit(-1)
login_body = {
    "uid": wxOpenId,
    "avatar": avatar,
    "nick_name": "1",
    "token": sacrifice_t,
    "sex": 1                
}
print("login_body：{}".format(login_body))


login_res = requests.post(user_login_api, headers=request_header, json=login_body, timeout=15, verify=False)
print("login_res：{}".format(str(login_res.json())))
user_token = login_res.json()["data"]["token"]