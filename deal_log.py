import json
import re
from datetime import datetime


def s_timestamp2timeStr(s_timestamp):
  

    # 转换为本地时间
    local_time = datetime.fromtimestamp(s_timestamp)

    # 输出本地时间
    print(local_time)

    # 如果需要特定格式的时间字符串，可以使用strftime方法
    formatted_time = local_time.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time


def matchValue(reStr, sourceContent, matchIndex):
    pat = re.compile(reStr) #用()表示1个组，2个组
    m = pat.search(sourceContent)
    if m == None:
        return 
    return m.group(matchIndex) #默认为0，表示匹配整个字符串


def deal_log():
    lines = open(file="C:\\Users\syske\\Downloads\\3179918b-ae4e-4a8e-afd1-206057ddc28a.json", encoding="utf-8").readlines()
    for line in lines:
        log = json.loads(line)
        time = log['__time__']
        content = log['content']
        contentJsonStr = matchValue(r'content=({.*?})', content, 1)
        #print(s_timestamp2timeStr(int(time)), contentJsonStr)
        print(contentJsonStr)

if __name__ == "__main__":
    deal_log()