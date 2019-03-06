from ClauseAnalysis.FilePreprocess import *
from ClauseAnalysis.SentenceExtractor import *
import re


critical_words = []


def sentence_filter(sentences):
    good_sentences = []
    bad_sentences = []
    for sentence in sentences:
        if contains_critical_word(sentence):
            good_sentences.append(sentence)
        else:
            bad_sentences.append(sentence)
    return good_sentences, bad_sentences


def read_critical_words():
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "criticalWords.txt")
    file_open = open(file_path, 'r', encoding='UTF-8')
    file_text = file_open.read()
    content_string = str(file_text)

    global critical_words
    critical_words = content_string.split("\n")

    # Traversing through critical_words in reversed order
    for index in list(range(len(critical_words)-1, -1, -1)):
        if not critical_words[index] or critical_words[index][0] == '#':
            critical_words.remove(critical_words[index])


def contains_critical_word(sentence):
    is_contained = False
    for criticalWords in critical_words:
        search_result = re.search(r'' + criticalWords + '', sentence, re.I)
        if search_result:
            is_contained = True
            # print(criticalWords)
            break
    return is_contained


class SentenceFilter:
    sentence_array = ''

    def __init__(self, sentenceArray):
        self.sentence_array = sentenceArray
        read_critical_words()

    def execute(self):
        return sentence_filter(self.sentence_array)


if __name__ == '__main__':

    filePreprocess = FilePreprocess("licenseTestCase1")
    input_file = filePreprocess.execute()

    sentenceExtractor = SentenceExtractor(input_file)
    sentences_extracted = sentenceExtractor.execute()

    sentenceFilter = SentenceFilter(sentences_extracted)
    goodSentences, badSentences = sentenceFilter.execute()
    for g in goodSentences:
        print(g)
