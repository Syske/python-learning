import time,json,logging
import re
from datetime import datetime
import pandas as pd

def matchValue(reStr, sourceContent, matchIndex):
    pat = re.compile(reStr) #用()表示1个组，2个组
    m = pat.search(sourceContent)
    if m == None:
        return 
    return m.group(matchIndex) #默认为0，表示匹配整个字符串


def get_full_data():
    contents = ''
    lines = open(file="C:\\Users\\syske\\Downloads\\8582448c-78f6-486e-baf5-3f4f29ae1ece.json", encoding="utf-8").readlines()
    dataresult = []
    for line in lines:
        log = json.loads(line)
        time = log['__time__']
        content = log['content']
        datas = content.split('\r\n')
        for data in datas:
            if 'span.kind' not in data:
                continue
            dataJson = None
            # print(data)
            if "\\r" in data:
                dataJson = json.loads(data.replace('\\r', ''))
            else:
                dataJson = json.loads(data)
            dataresult.append({
                "local.app": dataJson['local.app'],
                "method": dataJson['method'], 
                "server.pool.wait.time" : int(dataJson.get('server.pool.wait.time', '0')), 
                "biz.impl.time": int(dataJson.get('biz.impl.time', '0')),
                "tracerId": dataJson.get('tracerId')
            })
            # print(dataJson['local.app'], dataJson['method'], dataJson.get('server.pool.wait.time'), dataJson.get('biz.impl.time'), dataJson.get('tracerId'))
        # dict_data = {'Ohio':35000,'Texas':72000,'Orgeon':16000,'Utah':5000}
    df = pd.DataFrame(dataresult)
    # print(df.head())
    df_sorted_asc = df.sort_values(by='biz.impl.time', ascending=False)
    print(df_sorted_asc)

def get_data_from_log():
    contents = ''
    lines = open(file="C:\\Users\\syske\\Downloads\\8582448c-78f6-486e-baf5-3f4f29ae1ece.json", encoding="utf-8").readlines()
    datas = []
    for line in lines:
        log = json.loads(line)
        time = log['__time__']
        content = log['content']
        #contentJsonStr = matchValue(r'content=({.*?})', content, 1)
        start_index = content.find('content={') + len('content=')
        # print(start_index, type(start_index))
        cont = content[start_index:]
        #print(s_timestamp2timeStr(int(time)), contentJsonStr)
        # print(cont)
        jsonContent = json.loads(cont)
        datas.append(jsonContent)
    return datas
        
def deal_data():
    contents = ''
    datas = get_data_from_log()
    for contetent_data in datas:
        # print(contetent_data)
        #timestamp = contetent_data[1]
        #data = contetent_data[0]
        #eid = data['enterpriseId']
        data_list = contetent_data['data']
        # print(timestamp)
        optType = contetent_data['optType']
        if optType != 'UPDATE':
                continue
        for binlog in data_list:
            if 'department' not in binlog:
                continue
            print(binlog)
            uid = binlog['id']['originVal']
            uid = binlog['id']['originVal']
            print(uid)
            department_orig = binlog['department']['originVal']
            department_currVal = binlog['department']['currVal']
            
            departments_orig = binlog['departments']['originVal']
            departments_currVal = binlog['departments']['currVal']
            contents += f'{uid}\t{department_orig}\t{department_currVal}\t{departments_orig}\t{departments_currVal}\n'
    open("dept_user_info_binlog.txt", mode='w+', encoding='utf-8').write(contents)
        

        

        
if __name__ == '__main__':
    # send_fxxk_msg()
    # deal_data()
    get_full_data()
