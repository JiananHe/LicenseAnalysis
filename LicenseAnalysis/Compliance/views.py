import json
import os
import sys
import time
import shutil

from django.http import HttpResponse
from django.shortcuts import render

import LicenseModel.models as LM
import Compliance.licenseContentAnalyse as LCA


def upload_file(myfile):
    nowTime = int(time.time())
    UploadFolder = sys.path[0] + os.sep + "UploadFiles"
    newPath = os.path.join(UploadFolder, myfile.name + str(nowTime))
    newFile = open(newPath, 'wb+')
    for chunk in myfile.chunks():
        newFile.write(chunk)
    newFile.close()

    fob = open(newPath)
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

    dir_stack = []
    dir_name = ""
    file_id = 0
    for file in myfolder:
        file_id = file_id + 1
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
        fob = open(new_file_path)
        text = str(fob.read())
        new_file.close()

        licenseId, tmp = LCA.contentAnalysis(text)

        # get license id
        licenseAbbr = LM.getLicenseAbbr(licenseId)

        files_content[str(file_tag)] = json.dumps(tmp)

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

    # tree_content += r'<span><i class="icon-folder-open"></i> 顶级节点1</span> <a onclick=showContent(' + str(file_id) +')>Abbreviation</a>'
    tree_content += r'</ul>'

    # avoid character transferred
    # files_content = str(files_content).encode("unicode-escape")
    # files_content=str(files_content).replace("\'", "\"")
    return files_content, tree_content


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
            files_content, tree_content = upload_folder(myfolder)

            # print("======================== " + tree_content)
            # print("======================== " + str(files_content))
            return render(request, "compliance.html", {'hidden1': "", 'hidden2': "Hidden",
                                                       'files_content': files_content,
                                                       'tree_content': tree_content})
        elif myfile:
            text = upload_file(myfile)
            print("============= user file text : " + text)
            id, result = LCA.contentAnalysis(text)
            return render(request, "compliance.html", {'result': json.dumps(result),
                                                       'hidden1': "Hidden",
                                                       'hidden2': ""})
        elif text != "":
            text = str(text)
            print("========== use input text : " + text)
            id, result = LCA.contentAnalysis(text)
            return render(request, "compliance.html", {'result': json.dumps(result),
                                                       'hidden1': "Hidden",
                                                       'hidden2': ""})
        else:
            return render(request, "compliance.html", {'hidden1': "Hidden", 'hidden2': "Hidden"})

    else:
        return render(request, "compliance.html", {'hidden1': "Hidden", 'hidden2': "Hidden"})
