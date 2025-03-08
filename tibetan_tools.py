# -*- coding: utf-8 -*
# 藏文分詞及表格化

INPUTSTR = '''
བཀྲ་ཤིས་བདེ་ལེགས། ཞོགས་པ་བདེ་ལེགས།
ཁྱེད་རང་གང་འདྲ་འདུག ཧ་ཅང་ཡག་པོ་འདུག
'''

COL_NUM = 10    # md表格列數

def split_tibetan(raw_str):
    '''
    將標準藏文進行分詞，返回詞句的嵌套List
    藏文按規則進行分詞，分句使用空格或回車
    輸入：'བཀྲ་ཤིས་བདེ་ལེགས། ཞོགས་པ་བདེ་ལེགས།\nཁྱེད་རང་གང་འདྲ་འདུག ཧ་ཅང་ཡག་པོ་འདུག'
    輸出：[
        ['བཀྲ་', 'ཤིས་', 'བདེ་', 'ལེགས།'],
        ['ཞོགས་', 'པ་', 'བདེ་', 'ལེགས།'],
        ['ཁྱེད་', 'རང་', 'གང་', 'འདྲ་', 'འདུག'],
        ['ཧ་', 'ཅང་', 'ཡག་', 'པོ་', 'འདུག']]
    '''
    tmpstr = ''
    last_char = ''
    for i,char in enumerate(raw_str):
        if last_char == '་' and char != '།':  # 分字
            tmpstr += '，'
        if char in ' \n':  # 空格分句
            if last_char not in '་། ':
                tmpstr += '。'
                last_char = char
            continue
        tmpstr += char
        if char == '།':  # 分句
            tmpstr += '。'
        last_char = char
    # print(tmpstr)
    result = []
    sentences = tmpstr.split('。')
    for sentence in sentences:
        if not sentence: continue
        words = sentence.split('，')
        result.append(words)
    return result

def output_as_md(list_tibetan, col_num = 10):
    '''
    將格式化的藏文列表以markdown表格形式輸出
    '''
    result = ''
    this_line_len = 0   # 當前行字數
    this_line = ''  # 當前行內容
    is_header_added = False # 是否已添加表頭分隔（一次性）
    for sentence in list_tibetan:
        for num, word in enumerate(sentence):
            if num == len(sentence) - 1:    # 句尾最後一詞添加空格記號
                word += ' '
            if this_line_len >= col_num:    # 需要先換行
                result += this_line[:-1] + '\n' # 添加本行內容
                if not is_header_added: # 還沒加表頭分隔
                    header = '--|' * (col_num - 1) + '--\n'
                    result += header
                    is_header_added = True
                result += '|' * (col_num - 1) + '\n'    # 對照行
                this_line_len = 0
                this_line = ''
            # 添加新字
            this_line += word + '|'
            this_line_len += 1
    if this_line:   # 輸出未完成的補全
        result += this_line + '|' * (col_num - this_line_len - 1) + '\n'
        if not is_header_added: # 還沒加表頭分隔
            header = '--|' * (col_num - 1) + '--\n'
            result += header
        result += '|' * (col_num - 1) + '\n'    # 對照行
    return result

if __name__ == "__main__":
    result = split_tibetan(INPUTSTR)
    md_result = output_as_md(result)
    print('md:', md_result)
    # 還原原句
    ori_str = ''
    for num, line in enumerate(md_result.split('\n')):
        if num % 3 == 0:
            ori_str += line[:-1].replace('|','')
    print('ori_str:', ori_str)