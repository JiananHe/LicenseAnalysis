import pandas as pd
import numpy as np

class Conflict(object):
    def __init__(self,licenses,amount):
        self.amount=amount
        self.lics={}
        for i in range(self.amount):
            self.lics[i]=licenses[i]-1

    def detect(self):
        #取出兼容矩阵
        A = pd.read_csv('newAMatrix.csv', index_col=0)
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
                counter=counter+1
                cpResult[counter]=i+1
            isCp=True

        return cpResult


if __name__=="__main__":
    licenses={}
    licenses[0]=9
    licenses[1]=5
    licenses[2]=14
    conflict=Conflict(licenses,len(licenses))
    result=conflict.detect()
    print(result)

