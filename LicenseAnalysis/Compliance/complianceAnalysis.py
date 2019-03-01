import pandas as pd
import numpy as np
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'LicenseAnalysis.settings'
import django
django.setup()

# Get the path of this file
CURRENT_DIR = os.path.split(os.path.realpath(__file__))[0]

import LicenseModel.models as LM


class Compliance(object):
    def __init__(self, licenses):
        print("The id of the license that needs to be analyzed for compatibility is \n " + str(licenses))
        self.lics = licenses
        self.amount = len(licenses)

    def get_compatible_licenses(self):
        # csv file is under the same path with this py
        A = pd.read_csv(os.path.join(CURRENT_DIR, "newAMatrix.csv"))

        cpMatrix = np.copy(A.values)

        counter = 0
        cpResult = {}
        n = len(A)
        for i in range(n):
            isCp = True
            for j in range(self.amount):
                if cpMatrix[self.lics[j] - 1][i] == 1 or cpMatrix[self.lics[j] - 1][i] == -1:
                    continue
                else:
                    isCp = False
                    break
            if (isCp == True):
                cpResult[counter] = i
                counter = counter + 1
            isCp = True

        return cpResult

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
        print("the licenses id in csv file (self.lics)  is")
        print(self.lics)
        compatible_licenses_csv_id = self.get_compatible_licenses()
        print("the compatible_licenses_csv_id licenses is")
        print(compatible_licenses_csv_id)
        compatible_licenses = self.convert_csv_id_to_main_id(compatible_licenses_csv_id)
        return compatible_licenses


if __name__ == "__main__":
    licenses = {}
    # licenses[0]=9
    # licenses[1]=5
    # licenses[2]=14
    licenses[0] = 3
    licenses[1] = 19

    conflict = Compliance(licenses)
    result = conflict.get_compatible_licenses_processed()


