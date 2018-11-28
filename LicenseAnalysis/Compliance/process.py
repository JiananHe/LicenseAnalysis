from Compliance.func import *

o2t = []  # convert the corresponding position, original text --> trimmed  text
t2o = []  # convert the corresponding position, trimmed  text --> original text
# version_postfix = ['international', 'universal', 'c']
# model = "General Public License version 2"
# text = "under the terms of the GNU Generel Public License test_chararcter version 2 as published by the Free Software Foundation."


def trim_space(pre):
    """
    去掉多余的空格，并记录原字符串和处理后的字符串中每个字母的位置对应关系，存储在 o2t 和 t2o 两个数组中
    remove the redundant space, and record corresponding relationship with position on every vocabulary
    :param pre:
    :return:
    eg. the original text is: General Public License version 2
        the trimmed  text is: GeneralPublicLicenseversion2
    """
    post = ''
    length = len(pre)
    count = 0
    o2t.clear()
    t2o.clear()
    for i in list(range(0, length)):
        if pre[i] != ' ':
            post += pre[i]
            o2t.append(count)
            t2o.append(i)
            count = count + 1
        else:
            o2t.append(-1)
    return post


def text_process(text, model, version):
    """

    :return:
    """
    trimmed_text = trim_space(text)
    text_length = len(text)
    model_list = model.split()
    count = 0
    text_matched = False
    head = tail  = -1
    model_length = len(model_list)
    i = 0
    while i < text_length and i < len(o2t):
        # if the character text[i] is the first character of one word
        if text[i] != ' ' and (i == 0 or text[i-1] == ' '):
            model_word = model_list[count]
            start = o2t[i]
            end = start + len(model_word)
            text_word = trimmed_text[start:end]
            # word2 = text[i:text_length+1].split()[0]
            # print(i)
            # print(model_word)
            # print(text_word)
            dis = levenshtein_distance(model_word, text_word)
            # if satisfy the difference degree(or the similarity degree)
            if len(model_word)==0 or len(text_word)==0:
                count = 0
                i = i + 1
            elif dis/min(len(model_word), len(text_word)) < 0.2:
                # record the start position of the license
                if count == 0:
                    head = i
                # ‘o2t[i]+len(model_word)-1’ means the position of
                # the final character of the word in the trimmed text
                i = t2o[o2t[i]+len(model_word)-1] + 1
                count = count + 1
                # if the words of model license matched completely
                if count == model_length:
                    # record the end position of the license
                    tail = i
                    text_matched = True
                    break
            # if do not satisfy
            else:
                count = 0
                i = i + 1
        # if not the first character, then next character
        else:
            i = i + 1

    # if the license does not have the version information
    if version == '':
        if text_matched:
            return [True, head, tail, -1, -1]
        else:
            return [False, -1, -1, -1, -1]
    # if the license has have the version information
    else:
        if i >= text_length or i >= len(o2t):
            return [False, -1, -1, -1, -1]
        # now, the i point to the next character of the tail of the license string
        next_char_position = t2o[o2t[i-1] + 1]
        if text[next_char_position].isdigit():
            text_version = get_version(text[next_char_position: next_char_position+10])
        else:
            have_version = False
            while i < text_length:
                if text[i] == 'v' or text[i] == 'V':
                    text_version = get_version(text[i: i+20])
                    if not text_version[0] == -1:
                        have_version = True
                        break
                i = i + 1
            if have_version == False or text_version[0] == -1:
                return [False, -1, -1, -1, -1]
        model_version = get_version(version)
        if float(model_version[0]) == float(text_version[0]):
            return [True, head, tail, i+text_version[2], i+text_version[3]]
        elif (float(model_version[0]) < float(text_version[0])) and model_version[1]:
            return [True, head, tail, i + text_version[2], i + text_version[3]]
        else:
            return [False, -1, -1, -1, -1]


def model_process(model_string):
    model_split = model_string.split('#')
    model_license_number = model_split[0]

    model_text = model_split[1].split('|')[0]
    model_text = model_text.strip()
    return [model_license_number, model_text]


if __name__ == '__main__':
    aa = "V1.1# European Union Public Licence| EUPL"
    re = model_process(aa)
    print(re[0])
    print(re[1])
#
#     result_model = model_process("version 2.0 # General Public License")
#     print(result_model[1])
#     result_process = text_process(result_model[1], result_model[0])
#     print(result_process)
#     tmp = text
#     if result_process[0]:
#         if result_process[3] != -1:
#             tmp = tmp[0:result_process[3]] + '**' + tmp[result_process[3]:result_process[4]] + '**' + tmp[result_process[4]:len(tmp)]
#         tmp = tmp[0:result_process[1]]+'**'+tmp[result_process[1]:result_process[2]]+'**'+tmp[result_process[2]:len(tmp)]
#     print(tmp)
#     print(text)