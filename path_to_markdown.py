import os

rootdir = './'

ignorePathList = ['.git', '.obsidian', '.gitignore', 'README.md', 'markdown-symmary.py', '.trash']

def generate_markdown_tree(root_dir, markdown_file):
    global rootdir
    rootdir = root_dir
    with open(markdown_file, 'w', encoding='utf-8') as md:
        # 写入标题
        md.write("# 目录\n\n")
        # 调用递归函数
        _generate_tree_recursive(root_dir, md, 0)

def _generate_tree_recursive(current_dir, md, level):
    entries = os.listdir(current_dir)
    entries.sort()  # 可选：按字母顺序排序
    for entry in entries:
        if entry in ignorePathList:
                print('ignore dir')
                continue
        path = os.path.join(current_dir, entry)
        relative_path = os.path.relpath(path, start=rootdir)
        # print(path, rootdir, relative_path)
        print(level, entry)
        if os.path.isdir(path):
            # if level == 1:
            #     #print('### %s\n' %(i))
            #     md.write('### %s\n' %(entry))
            # elif md == 2:
            #     #print('#### %s\n' %(i))
            #     md.write('#### %s\n' %(entry))
            # elif level == 3:
            #     #print('##### %s\n' %(i))
            #     md.write('##### %s\n' %(entry))
            # else:
            #     #print('###### %s\n' %(i))
            #     md.write('###### %s\n' %(entry)) 
            md.write(f"{'#' * (level + 2)} {entry}\n")
            
            # 如果是目录，则写入目录条目
            # md.write(f"{'  ' * level}- [{entry}]({relative_path.replace(os.path.sep, '/')})\n")
            _generate_tree_recursive(path, md, level + 1)
        elif os.path.isfile(path):
            md.write(f"{'  ' * level}- [{entry}]({relative_path.replace(os.path.sep, '/')})\n")

# 指定目录和输出文件
root_directory = 'D:/workspace/learning/person-learning-note'
output_markdown_file = 'markdown.md'

# 生成Markdown树
generate_markdown_tree(root_directory, output_markdown_file)