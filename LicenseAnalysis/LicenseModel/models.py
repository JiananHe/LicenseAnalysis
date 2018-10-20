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
        result_list = license_description.objects.all()
    else:
        # search specific licenses
        result_list = license_description.objects.filter(abbreviation__icontains=search_text)

    for entry in result_list:
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
    result_list = license_description.objects.get(abbreviation=search_text)
    return {'name': result_list.name, 'abbreviation': result_list.abbreviation, 'content': result_list.content}