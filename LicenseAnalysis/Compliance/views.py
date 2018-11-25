import json
import os
import sys
import time

from django.http import HttpResponse
from django.shortcuts import render

import Compliance.licenseContentAnalyse as LCA


def upload_file(myfile):
    nowTime = int(time.time())
    UploadFolder = sys.path[0]+os.sep+"UploadFiles"
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
    return "2"


# Create your views here.
def index(request):
    if request.POST:
        # user upload a folder
        myfolder = request.FILES.getlist("user_folder", None)
        if myfolder:
            upload_folder(myfolder)
            return

        # user upload a file
        myfile = request.FILES.get("user_file", None)
        if myfile:
            text = upload_file(myfile)
            print("============= user file text : " + text)
            result = LCA.contentAnalysis(text)
            return render(request, "compliance.html", {'result': json.dumps(result),
                                                       'hidden1': "Hidden",
                                                       'hidden2': ""})

        # user input license content
        text = request.POST['user_input']
        if text != "":
            text = str(text)
            print("========== use input text : " + text)
            result = LCA.contentAnalysis(text)
            return render(request, "compliance.html", {'result': json.dumps(result),
                                                       'hidden1': "Hidden",
                                                       'hidden2': ""})


    else:
        # ctx['hidden'] = "hidden"
        return render(request, "compliance.html", {'hidden1': "Hidden", 'hidden2': "Hidden"})
