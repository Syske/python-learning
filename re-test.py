import re
import base64

def matchValue(reStr, sourceContent, matchIndex):
    pat = re.compile(reStr) #用()表示1个组，2个组
    m = pat.search(sourceContent)
    if m == None:
        return 
    return m.group(matchIndex) #默认为0，表示匹配整个字符串

if __name__ == '__main__':

    content = '''
    var vid="126447";var vfrom="3";var vpart="0"; var now=base64decode("aHR0cHM6Ly92aXAuZmZ6eXJlYWQuY29tLzIwMjMxMjA4LzIwNjY1XzJmYmQyNjU5L2luZGV4Lm0zdTg==");var pn="ffm3u8";var next=base64decode("aHR0cHM6Ly92aXAuZmZ6eXJlYWQuY29tLzIwMjMxMjA4LzIwNjY2XzA1NDVmZTgzL2luZGV4Lm0zdTg=");var prePage="/video/?126447-3-0.html";var nextPage="/video/?126447-3-1.html";
    '''

    reStr = r'now=base64decode\(\"(\w+\S+)\"\)'
    values = matchValue(reStr, content, 1)
    print(values)
    nowVidUrl = str(base64.b64decode('aHR0cHM6Ly92aXAuZmZ6eXJlYWQuY29tLzIwMjMxMjA4LzIwNjgxXzZiODgzNGYxL2luZGV4Lm0zdTg='), 'utf8')
    print(nowVidUrl)