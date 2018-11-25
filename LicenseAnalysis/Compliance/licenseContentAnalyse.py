from Compliance.process import *
import threading
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'LicenseAnalysis.settings'
import django

django.setup()
import LicenseModel.models as LM


class MyThread(threading.Thread):

    def __init__(self, thread_id, text, lic):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.text = text
        self.lic = lic
        self.result = []

    def run(self):
        # print("开始线程：" + str(self.thread_id))
        self.result = extract_license_info(self.text, self.lic)
        self.result.append(self.thread_id + 1)
        # print("退出线程：" + str(self.thread_id))

    def get_result(self):
        try:
            # print(self.result)
            return self.result
        except Exception:
            return None


def extract_license_info(text, license):
    """
    Extract and analysis the license info in the text
    :param text: a long string, the content of a file
    :return: a long string, the analyzed text with some marks.
    """
    trim_space(text)

    result_model = model_process(license)

    # print(result_model[1])
    result_process = text_process(text, result_model[1], result_model[0])
    # print(result_process)
    return result_process


# Create your tests here.
def find_all_possible_license(text_origin):

    all_licenses_key = LM.getLicensesKey()

    is_detected = False
    threads = []
    for i in list(range(0, 35)):
        # print(i)
        if all_licenses_key[i] != 'null':
            thread_now = MyThread(i, text_origin, all_licenses_key[i])
            thread_now.start()
            threads.append(thread_now)
    for t in threads:
        t.join()
    for t in threads:
        detect_result = t.get_result()
        if detect_result == None:
            return [-1, -1, -1, -1, -1]
        if detect_result[0] == True:
            is_detected = True
            detection_info = [detect_result[5], detect_result[1], detect_result[2],
                              detect_result[3], detect_result[4]]
            # print(detection_info)
    if is_detected == False:
        detection_info = [-1, -1, -1, -1, -1]
    print("The detection_info is ", detection_info)
    return detection_info

def get_license_id(text):
    result_process = find_all_possible_license(text)
    return result_process[0]


# contentAnalysis
def generate_license_presentation(text):
    """
    Generate the text that can highlight the license text and license version in the web,
    according to the html format.
    :param text: a long string, the content of a file
    :return: the processed text
    """
    # database access object
    # all_licenses_key = LM.getLicensesKey()
    # print(type(all_licenses_key))
    # print(all_licenses_key)
    #
    # csv_id = LM.getLicenseCsvId(21)
    # print(type(csv_id))
    # print(csv_id)

    result_process = find_all_possible_license(text)
    # print(result_process)
    tmp = text
    if result_process[0] != -1:
        if result_process[3] != -1:
            tmp = tmp[0:result_process[3]] + '<mark>' + tmp[result_process[3]:result_process[4]] + \
                  '</mark>' + tmp[result_process[4]:len(tmp)]
        tmp = tmp[0:result_process[1]] + '<mark>' + tmp[result_process[1]:result_process[2]] + '</mark>' \
              + tmp[ result_process[2]:len(tmp)]
    print(text)
    print(tmp)

    return tmp

if __name__ == '__main__':
    print()
    text_origin_1 = "under the terms of the under the Academic Free License test_chararcter version 3.0 as published by the Free Software Foundation."
    text_origin_2 = "under the terms of the under the European Union Public Licence chararcter v1.1 aaa."
    bb = "under the terms of the under Microsoft Reciprocal License | Ms-RL"
    aa = "V.1.1# European Union Public Licence| EUPL"
    cc = "a"
    generate_license_presentation(cc)
    #id = get_license_id(cc)
    print(id)
    # all_licenses_key = LM.getLicensesKey()
    # print(type(all_licenses_key))
    # print(all_licenses_key)
    # print(all_licenses_key[0])