from Compliance.process import *
import threading
import os
os.environ['DJANGO_SETTINGS_MODULE']='LicenseAnalysis.settings'
import django
django.setup()
import LicenseModel.models as LM


class MyThread(threading.Thread):

    def __init__(self, thread_id, text, lic):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.text = text
        self.lic = lic
        self.result =[]

    def run(self):
        # print("开始线程：" + str(self.thread_id))
        self.result = contentAnalysis(self.text, self.lic)
        self.result.append(self.thread_id+1)
        # print("退出线程：" + str(self.thread_id))

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


def contentAnalysis(text, license):
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
def extract_license_info(text_origin):
    # print("test")
    # text_origin = "under the terms of the under the Academic Free License test_chararcter version 3.0 as published by the Free Software Foundation."
    # license_model = "version 3.0#under the Academic Free License"
    # license2 = "version 3#under the terms of the GNU Affero General Public License"
    # contentAnalysis(text_origin, license_model)

    all_licenses_key = LM.getLicensesKey()

    is_detected = False
    threads = []
    for i in list(range(0, 35)):
        #print(i)
        if all_licenses_key[i]!='null':
            thread_now = MyThread(i, text_origin, all_licenses_key[i])
            thread_now.start()
            threads.append(thread_now)
    for t in threads:
        t.join()
    for t in threads:
        detect_result = t.get_result()
        if detect_result[0]==True:
            is_detected = True
            detection_info = [detect_result[5], detect_result[1], detect_result[2],
                              detect_result[3], detect_result[4]]
            print(detection_info)
    if is_detected==False:
        detection_info = [-1, -1, -1, -1, -1]

    return detection_info


