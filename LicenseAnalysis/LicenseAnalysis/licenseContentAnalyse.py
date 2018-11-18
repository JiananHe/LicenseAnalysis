from LicenseAnalysis.process import *


def contentAnalysis(text):
    """
    Extract and analysis the license info in the text
    :param text: a long string, the content of a file
    :return: a long string, the analyzed text with some marks.
    """
    print(text)
    # your analysis process
    trim_space(text)
    result_model = model_process("version 2.0 # General Public License")

    print(result_model[1])
    result_process = text_process(text, result_model[1], result_model[0])
    print(result_process)
    tmp = text
    if result_process[0]:
        if result_process[3] != -1:
            tmp = tmp[0:result_process[3]] + '<mark>' + tmp[result_process[3]:result_process[4]] + \
                  '</mark>' + tmp[result_process[4]:len(tmp)]
        tmp = tmp[0:result_process[1]] + '<mark>' + tmp[result_process[1]:result_process[2]] + '</mark>' \
              + tmp[ result_process[2]:len(tmp)]
    print(tmp)

    return tmp


# contentAnalysis("under the terms of the GNU Generel Public License test_chararcter version 2 as published by the Free Software Foundation.")