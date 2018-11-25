from django.db import models


# Create your models here.
class license_description(models.Model):
    name = models.CharField(max_length=20)
    abbreviation = models.CharField(max_length=10)
    synopsis = models.TextField(null=True)
    content = models.TextField(null=True)
    permissions = models.IntegerField(null=True)
    conditions = models.IntegerField(null=True)
    limitations = models.IntegerField(null=True)
    # add for compliance code
    text_key = models.TextField(null=True)
    # add for conflict code
    csv_id = models.IntegerField(null=True)


class permission(models.Model):
    name = models.CharField(max_length=50)
    meaning = models.TextField(null=True)


class condition(models.Model):
    name = models.CharField(max_length=50)
    meaning = models.TextField(null=True)


class limitation(models.Model):
    name = models.CharField(max_length=50)
    meaning = models.TextField(null=True)


def search_permissions(permission_num):
    """
    Return detailed permission info according to a permission number
    """
    search_result = []
    entry_count = permission.objects.all().count()
    for i in range(entry_count):
        if (permission_num >> i) & 1:  # treated as binary
            line = permission.objects.get(id=i + 1)
            tempEry = {'name': line.name, 'meaning': line.meaning}
            search_result.append(tempEry)

    return search_result


def search_conditions(condition_num):
    """
    Return detailed condition info according to a condition number
    """
    search_result = []
    entry_count = condition.objects.all().count()
    for i in range(entry_count):
        if (condition_num >> i) & 1:  # treated as binary
            line = condition.objects.get(id=i + 1)
            tempEry = {'name': line.name, 'meaning': line.meaning}
            search_result.append(tempEry)

    return search_result


def search_limitations(limitation_num):
    """
    Return detailed limitation info according to a limitation number
    """
    search_result = []
    entry_count = limitation.objects.all().count()
    for i in range(entry_count):
        if (limitation_num >> i) & 1:  # treated as binary
            line = limitation.objects.get(id=i + 1)
            tempEry = {'name': line.name, 'meaning': line.meaning}
            search_result.append(tempEry)

    return search_result


def searchLicense(search_text):
    """
    Search license info according to a regex of license name
    :param search_text: regex of license name
    :return: list of licenses' info
    """
    search_result = []

    print(search_text)
    if search_text == '':
        # if no search text, then return all license info
        entries = license_description.objects.all()
    else:
        # search specific licenses
        entries = license_description.objects.filter(abbreviation__icontains=search_text)

    for entry in entries:
        permissions = search_permissions(entry.permissions)

        conditions = search_conditions(entry.conditions)

        limitations = search_limitations(entry.limitations)

        tempEry = {'name': entry.name, 'abbreviation': entry.abbreviation, 'synopsis': entry.synopsis,
                   'permissions': permissions, 'conditions': conditions, 'limitations': limitations}
        search_result.append(tempEry)

    return search_result


def searchContent(search_text):
    """
    Search the full content according to a abbreviation of a license
    :param search_text: abbreviation of a license
    :return: the name, abbreviation and content of the license
    """
    entries = license_description.objects.get(abbreviation=search_text)
    return {'name': entries.name, 'abbreviation': entries.abbreviation, 'content': entries.content}


def getLicensesKey():
    """
    Return all licenses key
    :return:
    """
    entries = license_description.objects.values("text_key")
    return_list = []
    for entry in entries:
        return_list.append(entry["text_key"])

    return return_list


def getLicenseCsvId(id_num):
    """
    get the license id in csv file according to the standard id
    :param id_num: the standard license id in description table
    :return: the id in csv file
    """
    if id_num != -1:
        entry = license_description.objects.get(id=id_num)
        return entry.csv_id
    else:
        return ''

def getLicenseAbbr(id_num):
    if id_num != -1:
        entry = license_description.objects.get(id=id_num)
        return entry.abbreviation
    else:
        return 'no license'
