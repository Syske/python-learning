from itertools import zip_longest
 
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)
 
def split_string_by_length(s, length):
    return [''.join(chunk) for chunk in grouper(s, length, '')]
 
# 使用示例
original_string = open("C:\\Users\\syske\\Desktop\\eids.txt").read()
length_to_split = 19
split_strings = split_string_by_length(original_string, length_to_split)
 
print(split_strings, len(split_strings))  # 输出: ['Hello', 'World', 'ThisI', 'sATes', 'tStri', 'ng']