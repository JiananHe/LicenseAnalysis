import time
from django.http import HttpResponse
from django.shortcuts import render
import os, sys
import json

import LicenseModel.models as LM
import Compliance.licenseContentAnalyse as LCA
import Conflict.conflictDetect as LCD


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
            # remove the same license id
            is_license_exit = False
            for j in list(range(file_id)):
                if license_id_dict[j] == licenseId:
                    is_license_exit = True
                    break
            if is_license_exit == False:
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

    print("---------license_id_dict-------------")
    print(license_id_dict)
    print(len(license_id_dict))
    conflict_ditector= LCD.Conflict(license_id_dict, len(license_id_dict))
    conflict_result = conflict_ditector.detect()
    print("-------conflict_result-----------")
    print(conflict_result)

    existing_license_name_list = {}
    # existing_license_text = "在您上传的项目中检测到了 "
    existing_license_text = "The system detected " + str(len(license_id_dict)) + " license(s) in your project:  "
    for existing_id in list(range(len(license_id_dict))):
        # existing_license_name_list[existing_id] = LM.getLicenseName(license_id_dict[existing_id])
        name = LM.getLicenseName(license_id_dict[existing_id])
        if existing_id != 0:
            existing_license_text += ",    "
        existing_license_text += ( name + "  ")
    existing_license_text += ". "
    # existing_license_text += "等 " + str(len(license_id_dict)) + " 种许可证。"

    recommended_license_name_list = {}
    # recommended_license_text = "在您上传的项目中检测到了 "
    recommended_license_text = "The following licenses are recommended to compatible with all licenses in your project:   "
    for recommended_id in list(range(len(conflict_result))):
        # existing_license_name_list[existing_id] = LM.getLicenseName(license_id_dict[existing_id])
        name = LM.getLicenseName(conflict_result[recommended_id])
        if recommended_id != 0:
            recommended_license_text += ",    "
        recommended_license_text += ( name + "  ")
    recommended_license_text += ". "
    # recommended_license_text += "等 " + str(len(license_id_dict)) + " 种许可证。"


    return files_content, tree_content, existing_license_text, recommended_license_text # ,license_names


# Create your views here.
def index(request):
    if request.POST:
        myfolder = request.FILES.getlist("user_folder", None)
        print("folder name: " + str(myfolder))
        print("type is : " + str(type(myfolder)))

        # if len(myfolder):
        #     return HttpResponse("Upload failed")
        # result = LCA.contentAnalysis(text)

        if myfolder:
            print("----------upload_folder")
            files_content, tree_content, existing_license_text, recommended_license_text = upload_folder(myfolder)



            return render(request, "conflict.html", {'hidden': "",
                                                     'files_content': files_content,
                                                     'existing_license_text': existing_license_text,
                                                     'recommended_license_text': recommended_license_text,
                                                     'tree_content': tree_content})
        else:
            return render(request, "conflict.html", {'hidden': "Hidden"})

        # return render(request, "conflict.html", {'result': str(myfolder),
        #                                            'hidden': ""})
    else:
        # ctx['hidden'] = "hidden"
        return render(request, "conflict.html", {'hidden': "Hidden"})