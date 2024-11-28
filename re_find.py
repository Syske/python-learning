import re
from datetime import datetime

def matchValue(reStr, sourceContent, matchIndex):
    pat = re.compile(reStr) #用()表示1个组，2个组
    m = pat.search(sourceContent)
    if m == None:
        return 
    return m.group(matchIndex) #默认为0，表示匹配整个字符串


def get_data():
    lines = open(file="D:\\workspace\\note\\scrpit\\tools\\role_update_sql\\1372001210101534751_roles_upate.sql", encoding="utf-8").readlines()
    datas = ''
    for line in lines:
        content = matchValue(r'id =([0-9]*)', line, 1)
        print(content)
        datas += f'{content},'
    return datas[:-1] 
        
        
if __name__ == "__main__":
    datas = get_data()
    print(datas)