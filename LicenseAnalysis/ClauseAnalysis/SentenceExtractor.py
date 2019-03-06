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


# deal with comments /*, */ and //
def remove_blank_line(file_content):
    sentences_string = re.sub("[\n]+", "\n", file_content)
    sentences_string = re.sub("\n", ". ", sentences_string)
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
            # stitching_string += '. '
            stitching_string += sentence_array[i]
            if judge_contain_specific_words(current_sentence):
                need_stitching = True
            else:
                need_stitching = False
                # stitching_string += '.'
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
                new_array.append(sentence_array[i])
    return new_array


class SentenceExtractor():
    input_file = ''
    analyse_type = ''

    def __init__(self, inputFile):
        self.input_file = inputFile
        self.analyse_type = "comment"

    def set_analyse_type(self, type):
        self.analyse_type = type

    def execute(self):
        sentence = ''
        if self.analyse_type == "comment":
            sentence = remove_annotation_symbols(self.input_file)
        elif self.analyse_type == "text":
            sentence = remove_blank_line(self.input_file)
        else:
            print("Analyse Type Error: There is no such analyse_type.")
        # print(sentence)
        return split_sentence(sentence)


if __name__ == '__main__':
    filePreprocess = FilePreprocess("licenseTestBSD3.txt")
    input_file = filePreprocess.execute()

    sentenceExtractor = SentenceExtractor(input_file)
    sentenceExtractor.set_analyse_type("text")
    sentences_array = sentenceExtractor.execute()
    print(sentences_array)
    for s in sentences_array:
        print(s)
