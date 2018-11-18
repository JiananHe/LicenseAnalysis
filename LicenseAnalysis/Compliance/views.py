import time
import os
import sys
import json
from django.http import HttpResponse
from django.shortcuts import render
import LicenseAnalysis.licenseContentAnalyse as LCA


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
    return text


# Create your views here.
def index(request):
    if request.POST:
        text = request.POST['user_input']
        if text == "":
            myfile = request.FILES.get("user_file", None)
            if not myfile:
                return HttpResponse("no file and no text!")

            text = upload_file(myfile)

        result = LCA.contentAnalysis(text)

        return render(request, "compliance.html", {'result': json.dumps(result),
                                                   'hidden': ""})
    else:
        # ctx['hidden'] = "hidden"
        return render(request, "compliance.html", {'hidden': "Hidden"})
