import re


def get_version(initial_str):
    """
    extract the license version information, including the version number
        and the positions of the start and the end of the version number
    :param initial_str: the string that need to extract the license version information
    :return: [ version number, if exits '+', the start position, the end position ]
    """
    str = initial_str.replace(' ','')
    if str[0:7] == 'version' and str[7].isdigit():
        # version_number = re.findall("\d+\.\d+|\d+", str[7:length])[0]
        # print(str[7:length])
        first_iter = list(re.finditer(r'\d+\.\d+|\d+', initial_str))[0]
        version_number = first_iter.group()
        version_span = first_iter.span()
    elif (str[0] == 'v' or str[0] == 'V') and str[1].isdigit():
        first_iter = list(re.finditer(r'\d+\.\d+|\d+', initial_str))[0]
        version_number = first_iter.group()
        version_span = first_iter.span()
    elif str[0].isdigit():
        first_iter = list(re.finditer(r'\d+\.\d+|\d+', initial_str))[0]
        version_number = first_iter.group()
        version_span = first_iter.span()
    else:
        return [-1,False,-1,-1]

    if version_span[1]+1 < len(initial_str) and initial_str[version_span[1]] == '+':
        return [version_number, True, 0, version_span[1]]
    else:
        return [version_number, False, 0, version_span[1]]

    # initial_length = len(initial_str)
    # length = len(str)
    # possible_postfix_list = initial_str[version_span[1]:initial_length].split()
    # # if the possible_postfix_list is empty
    # if not len(possible_postfix_list):
    #     return [version_number,-1]
    # possible_postfix = possible_postfix_list[0]
    # # print(possible_postfix)
    #
    # postfix_number = -1
    # for i in list(range(0,len(version_postfix))):
    #     if version_postfix[i] == possible_postfix:
    #         print(possible_postfix)
    #         print(version_postfix[i])
    #         postfix_number = i
    #         break
    # return [version_number, postfix_number]
    # print(version_number)
    # print(version_span[0])
    # print(version_span[1])
    # print("final")


def levenshtein_distance(first, second):
    """
    计算两个字符串之间的L氏编辑距离
    calculate the Levenshtein Distance between two strings
    :param first:  the first string
    :param second: the second string
    :return: the Levenshtein Distance
    """
    if len(first) == 0 or len(second) == 0:
        return len(first) + len(second)
    first_length = len(first) + 1
    second_length = len(second) + 1
    distance_matrix = [[i+j for j in list(range(second_length))] for i in list(range(first_length))]  # 初始化矩阵
    for i in list(range(1, first_length)):
        for j in list(range(1, second_length)):
            deletion = distance_matrix[i-1][j] + 1
            insertion = distance_matrix[i][j-1] + 1
            substitution = distance_matrix[i-1][j-1]
            if first[i-1] != second[j-1]:
                substitution += 1
            distance_matrix[i][j] = min(insertion, deletion, substitution)
    return distance_matrix[first_length-1][second_length-1]


if __name__ == '__main__':
    print(get_version('version 2.0 international'))
    print(get_version('version 2.0'))
    print(get_version('v2.0+ universal'))
    print(get_version('version 35+ 66'))
    print(get_version('35 + 66'))
    print(get_version('aaa 35 66'))

    print(levenshtein_distance("Mozilla", "Moz"))
    print(levenshtein_distance("Mozilla", "Mozi"))
    print(levenshtein_distance("hhhhhh", "h"))

    print(levenshtein_distance("hhhhhh", "h"))

    print(levenshtein_distance("h", "hhhhhh"))

    matrix = [[i+j for j in range(4)] for i in range(4)]
    print(matrix)
