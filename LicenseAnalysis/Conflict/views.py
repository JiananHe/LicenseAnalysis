import time
from django.http import HttpResponse
from django.shortcuts import render
import os, sys
import json

import LicenseModel.models as LM
import Compliance.licenseExtract as LE
import ClauseAnalysis.LicenseMatcher as LCM
import Compliance.complianceAnalysis as LCA



def upload_file(myfolder):
    for file in myfolder:
        print("each file name: " + file.name)


def treeHtmlCode(fileName, layer):
    code = r''
    if layer == 1:
        code += r'<li><span><i class="icon-folder-open"></i>' + str(fileName) + '</span><ul>'
    elif layer > 1:
        code += r'<li><span><i class="icon-minus-sign"></i>' + str(fileName) + '</span><ul>'
    else:
        code += r'</ul></li>'

    return code


def upload_folder(myfolder):
    # mkdir
    nowTime = int(time.time())
    savePath = sys.path[0] + os.sep + "UploadFiles" + os.sep + "folder" + str(nowTime)
    os.mkdir(savePath)

    # web tree structure html string
    tree_content = r'<ul>'
    # dict with all file name and its content after analysis
    files_content = {}
    # dict with all file name and its license name after analysis
    license_names = {}

    # license id list, archived for compliance detection
    license_id_list = []
    license_abbr_list = []

    dir_stack = []
    dir_name = ""
    file_id = 0
    for file in myfolder:
        file_tag = "file" + str(file_id)
        file_path = file.name
        file_id = file_id + 1
        print("each file name: " + file_path)
        path_list = file_path.split('/')

        # upload single file
        file_name = path_list[len(path_list) - 1]
        new_file_path = os.path.join(savePath, file_name)
        new_file = open(new_file_path, 'wb+')
        for chunk in file.chunks():
            new_file.write(chunk)
        new_file.close()

        fob = open(new_file_path, 'r', encoding='UTF-8')
        text = str(fob.read())

        # call the license extraction code 1.0
        licenseId, tmp = LE.generate_license_presentation(text)
        # call the license extraction code 2.0 if the old algorithm get -1
        if licenseId == -1:
            license_abbr = LCM.LicenseMatcherInterface(new_file_path)
            print("*******license analysis results with clause analysis*********" + str(license_abbr))
            licenseId = LM.getLicenseId(license_abbr)

        if not licenseId == -1:
            license_id_list.append(licenseId)

        # get license abbreviation
        licenseAbbr = LM.getLicenseAbbr(licenseId)
        if licenseAbbr != 'no license':
            license_abbr_list.append(licenseAbbr)

        files_content[str(file_tag)] = json.dumps(tmp)

        license_name = LM.getLicenseName(licenseId)
        license_name = '<a href="/license/introduction?search-text=' + \
                       licenseAbbr + '"><black>' + license_name + '</black></a>'
        license_names[str(file_tag)] = json.dumps(license_name)

        # record file directory structure
        dir_layer = 0
        for pt in path_list:
            print(pt)
            if pt == file_name:
                tree_content += r'<li><span><i class="icon-leaf"></i>' + str(
                    file_name) + '</span><a onclick=showContent("' + str(file_tag) + '")>' + str(
                    licenseAbbr) + '</a></li>'

            elif pt in dir_stack:
                dir_layer = dir_layer + 1
                continue
            elif dir_layer == len(dir_stack): # push
                dir_layer = dir_layer + 1
                dir_stack.append(pt)
                tree_content += treeHtmlCode(pt, dir_layer)
            else:  # pop olds then push new
                while dir_layer < len(dir_stack):
                    tree_content += treeHtmlCode('', -1)
                    dir_stack.pop()
                dir_layer = dir_layer + 1
                dir_stack.append(pt)
                tree_content += treeHtmlCode(pt, dir_layer)

    tree_content += r'</ul>'

    # call conflict  analysis code
    conflict_list = [['Y', 'Y', 'N', 'Y', 'Y', 'Y', 'Y'],
                     ['Y', 'Y', 'Y', 'N', 'Y', 'Y', 'Y'],
                     ['N', 'Y', 'Y', 'Y', 'Y', 'Y', 'N'],
                     ['Y', 'N', 'Y', 'Y', 'Y', 'Y', 'Y'],
                     ['Y', 'Y', 'Y', 'Y', 'Y', 'N', 'Y'],
                     ['Y', 'Y', 'Y', 'Y', 'N', 'Y', 'Y'],
                     ['Y', 'Y', 'N', 'Y', 'Y', 'Y', 'Y']]

    conflict_result = r'<table class="table">'
    conflict_result += r'<tbody>'
    conflict_result += r'<tr>'
    conflict_result += r'<td> </td>'
    for abbr in license_abbr_list:
        conflict_result += r'<td>' + r'<a href="/license/introduction?search-text=' + abbr + r'">' + abbr + r'</a></td>'
    conflict_result += r'</tr>'

    for i, abbr in enumerate(license_abbr_list):
        conflict_result += r'<tr>'
        conflict_result += r'<td>' + r'<a href="/license/introduction?search-text=' + abbr + r'">' + abbr + r'</a></td>'
        for ans in conflict_list[i]:
            conflict_result += r'<td>' + ans + r'</td>'
        conflict_result += r'</tr>'

    conflict_result += r'</tbody>'
    conflict_result += r'</table>'

    return files_content, tree_content, license_names, conflict_result


# Create your views here.
def index(request):
    if request.POST:
        # user upload a folder
        myfolder = request.FILES.getlist("user_folder", None)

        if myfolder:
            files_content, tree_content, license_names, conflict_result = upload_folder(myfolder)

            return render(request, "conflict.html", {'hidden1': "",
                                                       'files_content': files_content,
                                                       'license_names': license_names,
                                                       'tree_content': tree_content,
                                                       'conflict_result': json.dumps(conflict_result)})

        else:
            return render(request, "conflict.html", {'hidden1': "Hidden", 'hidden2': "Hidden"})

    else:
        return render(request, "conflict.html", {'hidden1': "Hidden", 'hidden2': "Hidden"})