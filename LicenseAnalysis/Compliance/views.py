import json
import os
import sys
import time
import shutil

from django.http import HttpResponse
from django.shortcuts import render

import LicenseModel.models as LM
import Compliance.licenseExtract as LCA
import Conflict.conflictDetect as LCD


def upload_file(myfile):
    nowTime = int(time.time())
    UploadFolder = sys.path[0] + os.sep + "UploadFiles"
    newPath = os.path.join(UploadFolder, myfile.name + str(nowTime))
    newFile = open(newPath, 'wb+')
    for chunk in myfile.chunks():
        newFile.write(chunk)
    newFile.close()

    fob = open(newPath, 'r', encoding='UTF-8')
    text = fob.read()
    newFile.close()
    return str(text)


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

    # license id dict(file_path: license_id), archived for conflict detection
    license_id_dict = {}

    dir_stack = []
    dir_name = ""
    file_id = 0
    for file in myfolder:
        file_tag = "file" + str(file_id)
        file_path = file.name
        print("each file name: " + file_path)
        path_list = file_path.split('/')

        # upload single file
        file_name = path_list[len(path_list) - 1]
        new_file_path = os.path.join(savePath, file_name)
        new_file = open(new_file_path, 'wb+')
        for chunk in file.chunks():
            new_file.write(chunk)
        new_file.close()

        # compliance analysis
        fob = open(new_file_path, 'r', encoding='UTF-8')
        text = str(fob.read())
        new_file.close()

        # call the compliance code
        licenseId, tmp = LCA.generate_license_presentation(text)
        if not licenseId==-1:
            license_id_dict[file_id] = licenseId
            file_id = file_id + 1


        # get license abbreviation
        licenseAbbr = LM.getLicenseAbbr(licenseId)

        files_content[str(file_tag)] = json.dumps(tmp)

        license_name = LM.getLicenseName(licenseId)
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
            else: # pop olds then push new
                while dir_layer < len(dir_stack):
                    tree_content += treeHtmlCode('', -1)
                    dir_stack.pop()
                dir_layer = dir_layer + 1
                dir_stack.append(pt)
                tree_content += treeHtmlCode(pt, dir_layer)

    tree_content += r'</ul>'

    # print("---------license_id_dict-------------")
    # print(license_id_dict)
    # print(len(license_id_dict))
    # conflict_ditector= LCD.Conflict(license_id_dict, len(license_id_dict))
    # conflict_result = conflict_ditector.detect()
    # print("-------conflict_result-----------")
    # print(conflict_result)
    conflict_result = ''
    return files_content, tree_content, license_names, conflict_result


# Create your views here.
def index(request):
    if request.POST:
        # user upload a folder
        myfolder = request.FILES.getlist("user_folder", None)
        # user upload a file
        myfile = request.FILES.get("user_file", None)
        # user input license content
        text = request.POST['user_input']

        if myfolder:
            files_content, tree_content, license_names, conflict_result = upload_folder(myfolder)

            return render(request, "compliance.html", {'hidden1': "", 'hidden2': "Hidden",
                                                       'files_content': files_content,
                                                       'license_names': license_names,
                                                       'tree_content': tree_content,
                                                       'conflict_result': json.dumps(conflict_result)})
        elif myfile:
            text = upload_file(myfile)
            # print("============= user file text : " + text)
            # print("========== the end of text : ")
            id, result = LCA.generate_license_presentation(text)
            license_name = LM.getLicenseName(id)
            return render(request, "compliance.html", {'result': json.dumps(result),
                                                       'license_name': json.dumps(license_name),
                                                       'hidden1': "Hidden",
                                                       'hidden2': ""})
        elif text != "":
            text = str(text)
            # print("========== use input text : " + text)
            # print("========== the end of text : ")
            id, result = LCA.generate_license_presentation(text)
            # print(result)
            license_name = LM.getLicenseName(id)
            return render(request, "compliance.html", {'result': json.dumps(result),
                                                       'license_name': json.dumps(license_name),
                                                       'hidden1': "Hidden",
                                                       'hidden2': ""})
        else:
            return render(request, "compliance.html", {'hidden1': "Hidden", 'hidden2': "Hidden"})

    else:
        return render(request, "compliance.html", {'hidden1': "Hidden", 'hidden2': "Hidden"})
