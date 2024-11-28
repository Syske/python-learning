import os

ignorePathList = ['.git', '.obsidian', '.gitignore', 'README.md', 'markdown-symmary.py', '.trash', 'LICENSE']

def tree(dir_path, md, prefix=0):
    contents = os.listdir(dir_path)
    
    # 将目录和文件分开并排序
    dirs = sorted([d for d in contents if os.path.isdir(os.path.join(dir_path, d))])
    files = sorted([f for f in contents if os.path.isfile(os.path.join(dir_path, f))])

    # 打印当前目录名
    # print(f"{prefix}+-- {os.path.basename(dir_path)}")
    prefix += 1

    # 先列出所有子目录
    for dir_name in dirs:
        if dir_name in ignorePathList:
            # print('ignore dir')
            continue
        dir_path_child = os.path.join(dir_path, dir_name)
        md.write(f"{'#' * (prefix + 1)} {dir_name}\n\n")
        tree(dir_path_child, md, prefix)

    # 最后列出所有文件
    # for file_name in files:
    for i, file_name in enumerate(files):
        if file_name in ignorePathList:
            # print('ignore dir')
            continue
        content_path = os.path.join(dir_path, file_name)
        relative_path = os.path.relpath(content_path, start=root_dir)
        # print(relative_path)
        md.write(f"{' ' * (prefix - 1)}- [{file_name}]({relative_path.replace(os.path.sep, '/')})\n")
        is_last = i == len(files) - 1
        if is_last:
            md.write('\n')


def generate_markdown_tree(root_dir, markdown_file):
    global rootdir
    rootdir = root_dir
    with open(markdown_file, 'w', encoding='utf-8') as md:
        # 写入标题
        md.write("# 目录\n\n")
        # 调用递归函数
        tree(root_dir, md, 0)
# 指定根目录
output_markdown_file = 'markdown.md'
root_dir = 'D:/workspace/learning/person-learning-note'
generate_markdown_tree(root_dir, output_markdown_file)