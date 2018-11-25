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


def upload_folder(myfolder):
    # mkdir
    nowTime = int(time.time())
    savePath = sys.path[0] + os.sep + "UploadFiles" + os.sep + "folder" + str(nowTime)
    os.mkdir(savePath)

    # web tree structure html string
    tree_content = r'<ul>'
    # dict with all file name and its content after analysis
    # files_content = {}
    return_dict = {}

    dir_stack = []
    dir_layer = 0
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

        return_dict[str(file_tag)] = tmp

        # record file directory structure
        for pt in path_list:
            print(pt)
            if pt == file_name:
                tree_content += r'<li><span><i class="icon-leaf"></i>file_name</span><a onclick=showContent("' + str(
                    file_tag) + '")>' + str(licenseAbbr) + '</a></li>'
            if pt in path_list:
                continue

    # tree_content += r'<span><i class="icon-folder-open"></i> 顶级节点1</span> <a onclick=showContent(' + str(file_id) +')>Abbreviation</a>'
    tree_content += r'</ul>'
    return_dict['tree_content'] = tree_content
    return return_dict


# Create your views here.
def index(request):
    if request.POST:
        # user upload a folder
        myfolder = request.FILES.getlist("user_folder", None)
        if myfolder:
            ctx = {'hidden1': "", 'hidden2': "Hidden"}
            ctx1 = upload_folder(myfolder)
            ctx = dict(ctx, **ctx1) # merge two dict

            # print("======================== " + tree_content)
            # print("======================== " + str(files_content))
            print(str(ctx))
            return render(request, "compliance.html", ctx)

        # user upload a file
        myfile = request.FILES.get("user_file", None)
        if myfile:
            text = upload_file(myfile)
            print("============= user file text : " + text)
            id, result = LCA.contentAnalysis(text)
            return render(request, "compliance.html", {'result': json.dumps(result),
                                                       'hidden1': "Hidden",
                                                       'hidden2': ""})

        # user input license content
        text = request.POST['user_input']
        if text != "":
            text = str(text)
            print("========== use input text : " + text)
            id, result = LCA.contentAnalysis(text)
            return render(request, "compliance.html", {'result': json.dumps(result),
                                                       'hidden1': "Hidden",
                                                       'hidden2': ""})


    else:
        # ctx['hidden'] = "hidden"
        return render(request, "compliance.html", {'hidden1': "Hidden", 'hidden2': "Hidden"})
