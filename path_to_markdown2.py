import os

ignorePathList = ['.git', '.obsidian', '.gitignore', 'README.md', 'markdown-symmary.py', '.trash', 'LICENSE']

def generate_markdown_tree(root_dir, markdown_file):
    global rootdir
    rootdir = root_dir
    with open(markdown_file, 'w', encoding='utf-8') as md:
        # 写入标题
        md.write("# 目录\n\n")
        # 调用递归函数
        tree_markdown(root_dir, md, 0)

def tree_markdown(dir_path, md, level=0):
    global root_dir
    
    contents = sorted(os.listdir(dir_path))

    for i, content in enumerate(contents):
        if content in ignorePathList:
            # print('ignore dir')
            continue
        content_path = os.path.join(dir_path, content)
        is_last = i == len(contents) - 1
        relative_path = os.path.relpath(content_path, start=root_dir)
        # print(relative_path)
        if os.path.isdir(content_path):
            # print("    " * level + "|-- " + content)
            md.write(f"{'#' * (level + 2)} {content}\n")
            tree_markdown(content_path, md, level + 1)
        else:
            md.write(f'{"    " * level}- [{content}]({relative_path})\n')

# 指定根目录
output_markdown_file = 'markdown.md'
root_dir = 'D:/workspace/learning/person-learning-note'
# 生成Markdown树
generate_markdown_tree(root_dir, output_markdown_file)