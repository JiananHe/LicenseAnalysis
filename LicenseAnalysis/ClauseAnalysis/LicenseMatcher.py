from ClauseAnalysis.FilePreprocess import *
from ClauseAnalysis.SentenceExtractor import *
from ClauseAnalysis.SentenceFilter import *
from ClauseAnalysis.SentenceTokenizer import *
import re

license_rules_arrays = []


def read_license_rules():
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "LicenseRules.txt")
    file_open = open(file_path, 'r', encoding='UTF-8')
    file_text = file_open.read()
    content_string = str(file_text)

    global license_rules_arrays
    license_rules = content_string.split("\n")

    # Traversing through critical_words in reversed order
    for index in list(range(len(license_rules) - 1, -1, -1)):
        # remove the blank line and comments(start with "#")
        if not license_rules[index] or license_rules[index][0] == '#':
            license_rules.remove(license_rules[index])
    for rule in license_rules:
        items = rule.split(":")
        rule_name = items[0]
        rule_tokenizer = items[1]
        rule_tokenizer_array = rule_tokenizer.split(",")
        rule_array = [rule_name, rule_tokenizer_array]
        license_rules_arrays.append(rule_array)
        # print(sentence)
        # print(items)


def contains_license_rule(rule_tokenizer_array, result_tokenizer_array):
    result_match = 0
    result_length = len(result_tokenizer_array)
    for rule_index in range(len(rule_tokenizer_array)):
        for result_index in range(result_match, result_length):
            # print(rule_index,result_index,result_length)
            if rule_tokenizer_array[rule_index] == result_tokenizer_array[result_index]:
                # print("equal")
                # print(rule_tokenizer_array[rule_index])
                # print(result_tokenizer_array[result_index])
                result_match = rule_index + 1
                break
            elif result_index == result_length - 1:
                # print("return false")
                return False
            else:
                # print("continue")
                continue
    return True


def license_match_analyse(result_tokenizer_array):
    for rules_array in license_rules_arrays:
        rule_tokenizer_array = rules_array[1]
        is_matched = contains_license_rule(rule_tokenizer_array, result_tokenizer_array)
        if is_matched:
            return rules_array[0]
    else:
        return None


class LicenseMatcher:
    tokenizer_result_array = []

    def __init__(self, tokenizerResultArray):
        self.tokenizer_result_array = tokenizerResultArray
        read_license_rules()

    def execute(self):
        return license_match_analyse(self.tokenizer_result_array)


def LicenseMatcherInterface(file_path):
    """
    the interface of license clause analysis, integrate all analysis processes.
    :param file_path: the path of file needed to be analysed
    :return: license_result: the license name of file
    """
    filePreprocess = FilePreprocess(file_path)
    input_file = filePreprocess.execute()

    sentenceExtractor = SentenceExtractor(input_file)
    sentenceExtractor.set_analyse_type("text")
    sentences_extracted = sentenceExtractor.execute()

    sentenceFilter = SentenceFilter(sentences_extracted)
    good_sentences, bad_sentences = sentenceFilter.execute()

    sentenceTokenizer = SentenceTokenizer(good_sentences)
    tokenizer_result_arrays = sentenceTokenizer.execute()

    licenseMatcher = LicenseMatcher(tokenizer_result_arrays)
    license_result = licenseMatcher.execute()

    return license_result


if __name__ == '__main__':
    # filePreprocess = FilePreprocess("licenseTestCase1")
    # input_file = filePreprocess.execute()
    #
    # sentenceExtractor = SentenceExtractor(input_file)
    # sentences_extracted = sentenceExtractor.execute()
    license_result = LicenseMatcherInterface(r'C:\Users\13249\Desktop\license.txt')
    print(license_result)