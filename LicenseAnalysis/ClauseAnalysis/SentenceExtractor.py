from ClauseAnalysis.FilePreprocess import *
import re


# deal with comments /*, */ and //
def remove_annotation_symbols(file_content):
    regex = re.compile("/\*(.*)\*/", re.S)
    # print(regex.findall(file_content))
    sentences_string = ""
    for annotation in regex.findall(file_content):
        sentences_string += re.sub("[\t\n* ]+", " ", annotation)
        # print(re.sub("[\t\n* ]+", " ", annotation))
    return sentences_string.strip()


def judge_contain_specific_words(judge_string):
    regex = re.compile("INC$", re.I)
    search_result = regex.search(judge_string)
    if search_result:
        return True
    else:
        return False


def split_sentence(sentences_string):
    pattern = r'\. |: '
    sentence_array = re.split(pattern, sentences_string)
    new_array = []
    need_stitching = False
    stitching_string = ''
    for i in range(len(sentence_array)):
        current_sentence = sentence_array[i].strip()

        if need_stitching:
            stitching_string += '. '
            stitching_string += sentence_array[i]
            if judge_contain_specific_words(current_sentence):
                need_stitching = True
            else:
                need_stitching = False
                stitching_string += '.'
                new_array.append(stitching_string)
                stitching_string = ''
        else:
            if judge_contain_specific_words(current_sentence):
                stitching_string += sentence_array[i]
                need_stitching = True
                continue
            need_stitching = False
            if current_sentence.isdigit():
                pass
            else:
                new_array.append(sentence_array[i] + '.')
    return new_array


class SentenceExtractor():
    input_file = ''

    def __init__(self, inputFile):
        self.input_file = inputFile

    def execute(self):
        sentence = remove_annotation_symbols(self.input_file)
        # print(sentence)
        return split_sentence(sentence)


if __name__ == '__main__':
    filePreprocess = FilePreprocess("licenseTestCase1")
    input_file = filePreprocess.execute()

    sentenceExtractor = SentenceExtractor(input_file)
    sentences_array = sentenceExtractor.execute()
    for s in sentences_array:
        print(s)
