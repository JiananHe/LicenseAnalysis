import pandas as pd
import numpy as np
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'LicenseAnalysis.settings'
import django
django.setup()
import LicenseModel.models as LM

class Conflict(object):
    def __init__(self,licenses,amount):
        self.amount=amount

        self.lics = licenses
        self.lics={}
        # print("--------self.amount-----------")
        # print(self.amount)
        for i in range(self.amount):
            # print(i)
            self.lics[i]=licenses[i]

    def get_compatible_licenses(self):
        # 取出兼容矩阵
        # 注意：地址必须写为绝对地址形式，而且用 / 表示间隔而不能用 \\
        # Attention：Addresses must be written as absolute addresses and must usr '/' instead of '\\'
        A = pd.read_csv("E:/Users/Ye/Desktop/SRTP_github/LicenseAnalysis/LicenseAnalysis/Conflict/newAMatrix.csv")

        cpMatrix=np.copy(A.values)

        counter=0
        cpResult={}
        n=len(A)
        for i in range(n):
            isCp=True
            for j in range(self.amount):
                if cpMatrix[self.lics[j]-1][i] == 1 or cpMatrix[self.lics[j]-1][i] == -1:
                    continue
                else:
                    isCp=False
                    break
            if(isCp==True):
                cpResult[counter] = i
                counter = counter + 1
            isCp=True

        return cpResult

        # please give me a text a result
        # print(str(self.lics))
        # result = "this is a test conflict text, after improving conflict detection code, please replace result as your code return value"
        # return result

    def convert_main_id_to_csv_id(self):
        count = 0
        lics_csv_id = {}
        for i in list(range(len(self.lics))):
            if self.lics[i] == -1:
                continue
            csv_id = LM.getLicenseCsvId(self.lics[i])
            if csv_id == -1:
                continue
            else:
                lics_csv_id[count] = csv_id
                count += 1
        self.amount = len(lics_csv_id)
        self.lics = lics_csv_id

    def convert_csv_id_to_main_id(self, compatible_licenses):
        count = 0
        lics_main_id = {}
        for i in list(range(len(compatible_licenses))):
            if compatible_licenses[i] == -1:
                continue
            csv_id = LM.getLicenseIdByCsvId(compatible_licenses[i])
            if csv_id == -1:
                continue
            else:
                lics_main_id[count] = csv_id
                count += 1
        return lics_main_id

    def get_compatible_licenses_processed(self):
        self.convert_main_id_to_csv_id()
        print("the self.lics licenses is")
        print(self.lics)
        compatible_licenses_csv_id = self.get_compatible_licenses()
        print("the compatible_licenses_csv_id licenses is")
        print(compatible_licenses_csv_id)
        compatible_licenses = self.convert_csv_id_to_main_id(compatible_licenses_csv_id)
        return compatible_licenses


if __name__=="__main__":
    licenses={}
    # licenses[0]=9
    # licenses[1]=5
    # licenses[2]=14
    licenses[0]=3
    licenses[1]=19
    print("the input licenses is")
    print(licenses)

    conflict = Conflict(licenses, len(licenses))
    result=conflict.get_compatible_licenses_processed()
    # result = "this is a test conflict text, after improving conflict detection code, please replace result as your code return value"


    print("the result licenses is")
    print(result)


    # # this is a parameter example, please take a dict type parameter as your code input
    # dict = {'test-folder/License': 14,
    #  'test-folder/folder1-B/License': 1,
    #  'test-folder/folder1-B/folder2-A/License': 24,
    #  'test-folder/folder1-A/License': -1}
    #

    #
    # # please give me a text a result
    #result=conflict.detect()
    # result = "this is a test conflict text, after improving conflict detection code, please replace result as your code return value"
    #
    # print(result)

