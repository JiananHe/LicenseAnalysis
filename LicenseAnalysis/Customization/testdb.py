import sys
sys.path.append("..")
import LicenseModel.models as LM


def testdb_insert():
    test1 = LM.license_description(name='licenseA')
    test1 = LM.license_description(abbreviation='lA')
    test1.save()


def testdb_search(name):
    result = ""

    # All datas
    list = LM.license_description.objects.all()
    for var in list:
        result += str(var.id) + ' ' + var.name + ' ' + var.abbreviation + '\n'

    print(result)
    return result
