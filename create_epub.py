from ebooklib import epub
import parsel
import re
import os
import datetime
 
 
def matchValue(reStr, sourceContent, matchIndex):
    pat = re.compile(reStr) #用()表示1个组，2个组
    m = pat.search(sourceContent)
    if m == None:
        return 
    return m.group(matchIndex) #默认为0，表示匹配整个字符串


# 创建EPUB文件的函数  
def create_epub(book_title, author, update, introduction, chapters_content, cover_image):  
    # 创建EPUB书籍对象  
    book = epub.EpubBook()  
  
    # 设置书籍的元数据  
    book.set_identifier('id123456') # 书籍的唯一标识符  
    # 封面
    book.set_cover(cover_image, open(cover_image, 'rb').read())
    book.set_title(book_title) # 书籍的标题  
    book.set_language('zh') # 书籍的语言  
    book.add_author(author) # 书籍的作者  
  
    # 创建 CSS 样式  
    css_text = '''  
    @namespace epub "http://www.idpf.org/2007/ops";    
    body {        font-family: "Times New Roman", Times, serif;    }    
    p {        text-indent: 2em; /* 设置段落首行缩进 */        margin-top: 0;        margin-bottom: 1em;    }    
    '''  
    # 创建一个 CSS 文件对象  
    style = epub.EpubItem(uid="style", file_name="style/style.css", media_type="text/css", content=css_text)  
    # 将 CSS 文件添加到 EPUB 书籍中  
    book.add_item(style)  
  
    # 创建前言页面  
    c1 = epub.EpubHtml(title='前言', file_name='intro.xhtml', lang='zh')  
    c1.content = f'<html><head></head><body><h1>{book_title}</h1><p>作者：{author}</p><p>{update}</p><p>简介：{introduction}</p></body></html>'  
    book.add_item(c1)  
  
    # 初始化书脊  
    spine = ['nav', c1]  
  
    # 添加章节  
    for index in sorted(chapters_content.keys()):  # 按键排序  
        chapter = chapters_content[index]  
        title = chapter['title']  
        content = chapter['content']  # 将内容包裹在 <p> 标签中  
        # 创建 EPUB 格式的章节  
        epub_chapter = epub.EpubHtml(title=title, file_name=f'chapter_{index + 1}.xhtml', lang='zh')  
        epub_chapter.content = f'<html><head><style type="text/css">{css_text}</style></head><body><h2>{title}</h2>{content}</body></html>'  
        book.add_item(epub_chapter)  
        spine.append(epub_chapter)  
  
    # 设置书脊  
    book.spine = spine  
  
    # 创建目录列表，开始时包括前言链接  
    toc = [epub.Link('intro.xhtml', '前言', 'intro')]  
    # 对于每个章节，添加一个章节链接到目录列表中  
    for index in sorted(chapters_content.keys()):  
        chapter = chapters_content[index]  
        title = chapter['title']  
        # 创建章节的链接对象  
        chapter_link = epub.Link(f'chapter_{index + 1}.xhtml', title, f'chapter_{index + 1}')  
        toc.append(chapter_link)  
  
    # 最后，将目录列表设置为书籍的 TOC    
    book.toc = tuple(toc)  
  
    # 添加必要的 EPUB 文件  
    book.add_item(epub.EpubNcx())  
    book.add_item(epub.EpubNav())  
  
    # 保存 EPUB 文件  
    epub_path = f'{book_title}.epub'  
    epub.write_epub(epub_path, book, {})  
    print(f"EPUB 文件已创建: {epub_path}")  
  
if __name__ == "__main__":
    
    # 确保 chapters_content 中的章节已按顺序下载完成后，调用 EPUB 生成函数  
    bookTitle = '《剑来》'
    author = '烽火戏诸侯'
    introduction = '《剑来》是连载于纵横中文网中一部网络玄幻小说，作者是烽火戏诸侯。大千世界，无奇不有。天道崩塌，我陈平安，唯有一剑，可搬山，断江，倒海，降妖，镇魔，敕神，摘星，摧城，开天。'
    dir_path = './剑来'
    cover_image= "c:\\Users\\syske\\Downloads\\66c792d6-00a2-4e59-991b-d8ab6f52f3be.jpeg"
    file_list = os.listdir(dir_path)
    file_list.sort()
    # print(file_list)
    dataMap = {}
    indexs = []
    for f in file_list: 
        data = f.split(' ')
        # print(data)
        indexs.append(data[0])
        dataMap[data[0]] =  f
    chapters_content = {}
    chapter_split = {84 : "第一卷 笼中雀", 178 : "第二卷 山水郎", 238 : "第三卷 金错刀", 295 : "第四卷 剑气近", 359 : "第五卷 道观道", 455: "第六卷 小夫子", 
                     515 : "第七卷 龙抬头", 570 : "第八卷 思无邪", 684 : "第九卷 天上月", 746 : "第十卷 远游客", 833 : "第十一卷 夜归人", 956 : "第十二卷 选官子",
                     1036 : "第十三卷 破天荒", 1088 : "第十四卷 定风波"}
    indexs.sort()
    index = 1
    for data in indexs:
        # print(data)
        if str(index) in dataMap:
            f = dataMap[str(index)]
            file = open(f"{dir_path}/{f}", encoding='utf-8')
            # title = f.split('.')[0]
            title = matchValue(reStr=r'[0-9]+\s+(.+)\.txt', sourceContent=f, matchIndex=1)
            # print(title_temp)
            content = file.read()
            content_split = content.split('<br>')
            # print(content_split)
            chapter1_content = ''
            chapter_content = {}
            for splitStr in content_split:
                after = re.sub(r'<.+>', "" , splitStr)
                after = after.replace('书书网 更新最快','')
                after = after.replace('书书网手机版 m.1pwx.com','')
                chapter1_content += f'<p style="text-indent: 2em;line-height: 2em;font-family: sans-serif;">{after}</p>'
            chapter_content['title'] = title
            chapter_content['content'] = chapter1_content
    
        # selector1 = parsel.Selector(content)
        # content_temp = selector1.css('#content::text').getall()
        # print(content_temp)
        chapters_content[index] = chapter_content
        if index in chapter_split.keys():
            now = datetime.datetime.now()
            update = now.strftime("%Y-%m-%d %H:%M:%S")
            # print(chapters_content)
            create_epub(chapter_split[index], author, update, introduction, chapters_content, cover_image)
            chapters_content = {}
        index += 1
    