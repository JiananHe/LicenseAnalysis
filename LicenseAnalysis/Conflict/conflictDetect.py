import pandas as pd
import numpy as np

class Conflict(object):
    def __init__(self,licenses,amount):
        self.amount=amount

        self.lics = licenses
        self.lics={}
        print("--------self.amount-----------")
        print(self.amount)
        for i in range(self.amount):
            print(i)
            self.lics[i]=licenses[i]-1

    def detect(self):
        # 取出兼容矩阵
        # 注意：地址必须写为绝对地址形式，而且用 / 表示间隔而不能用 \\
        # Attention：Addresses must be written as absolute addresses and must usr '/' instead of '\\'
        A = pd.read_csv("C:/Users/Ye/Desktop/SRTP_github/LicenseAnalysis/LicenseAnalysis/Conflict/newAMatrix.csv")

        cpMatrix=np.copy(A.values)

        counter=0
        cpResult={}
        n=len(A)
        for i in range(n):
            isCp=True
            for j in range(self.amount):
                if(cpMatrix[self.lics[j]][i]==1 or cpMatrix[self.lics[j]][i]==-1):
                    continue
                else:
                    isCp=False
                    break
            if(isCp==True):
                cpResult[counter] = i + 1
                counter = counter + 1
            isCp=True

        return cpResult

        # please give me a text a result
        # print(str(self.lics))
        # result = "this is a test conflict text, after improving conflict detection code, please replace result as your code return value"
        # return result

if __name__=="__main__":
    licenses={}
    licenses[0]=9
    licenses[1]=5
    licenses[2]=14
    conflict = Conflict(licenses, len(licenses))
    result=conflict.detect()
    # result = "this is a test conflict text, after improving conflict detection code, please replace result as your code return value"

    print(result)
    print(licenses)

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

