import os
import sys


def upload_file(file_path):
    # UploadFolder = sys.path[0] + os.sep + "UploadFiles"
    # file_path = os.path.join(sys.path[0], file_name)
    file_open = open(file_path, 'r', encoding='UTF-8')
    file_text = file_open.read()

    return str(file_text)


class FilePreprocess():
    file_name = ''

    def __init__(self, fileName):
        self.file_name = fileName

    def execute(self):
        return upload_file(self.file_name)


if __name__ == '__main__':
    filePreprocess = FilePreprocess(os.path.join(sys.path[0], "licenseTestBSD3.txt"))
    input_file = filePreprocess.execute()
    print(input_file)