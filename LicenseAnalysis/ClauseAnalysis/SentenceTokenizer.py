from ClauseAnalysis.FilePreprocess import *
from ClauseAnalysis.SentenceExtractor import *
from ClauseAnalysis.SentenceFilter import *
import re


license_sentences_array = []


def read_license_sentences():
    file_path = os.path.join(sys.path[0], "licenseSentence.txt")
    file_open = open(file_path, 'r', encoding='UTF-8')
    file_text = file_open.read()
    content_string = str(file_text)

    global license_sentences_array
    license_sentences = content_string.split("\n")

    # Traversing through critical_words in reversed order
    for index in list(range(len(license_sentences)-1, -1, -1)):
        if not license_sentences[index] or license_sentences[index][0] == '#':
            license_sentences.remove(license_sentences[index])
    for sentence in license_sentences:
        items = sentence.split(":")
        license_sentences_array.append(items)
        # print(sentence)
        # print(items)


def contains_license_sentence(sentence):
    for licenseSentenceArray in license_sentences_array:
        search_result = re.search(r'' + licenseSentenceArray[3] + '', sentence, re.I)
        if search_result:
            return licenseSentenceArray[0]
    else:
        return None


def sentence_tokenizer_analyse(sentences):
    tokenizer_array = []
    for sentence in sentences:
        tokenizer = contains_license_sentence(sentence)
        tokenizer_array.append(tokenizer)
    return tokenizer_array


class SentenceTokenizer:
    good_sentence_array = []

    def __init__(self, goodSentenceArray):
        self.good_sentence_array = goodSentenceArray
        read_license_sentences()

    def execute(self):
        return sentence_tokenizer_analyse(self.good_sentence_array)


if __name__ == '__main__':

    filePreprocess = FilePreprocess("licenseTestCase1")
    input_file = filePreprocess.execute()

    sentenceExtractor = SentenceExtractor(input_file)
    sentences_extracted = sentenceExtractor.execute()

    sentenceFilter = SentenceFilter(sentences_extracted)
    good_sentences, bad_sentences = sentenceFilter.execute()

    sentenceTokenizer = SentenceTokenizer(good_sentences)
    tokenizer_result_array = sentenceTokenizer.execute()
    for t in tokenizer_result_array:
        print(t)
