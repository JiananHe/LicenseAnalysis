import time
from django.http import HttpResponse
from django.shortcuts import render
import os, sys


def upload_file(myfolder):
    for file in myfolder:
        print("each file name: " + file.name)


# Create your views here.
def index(request):
    if request.POST:
        myfolder = request.FILES.getlist("user_folder", None)
        print("folder name: " + str(myfolder))
        print("type is : " + str(type(myfolder)))

        # if len(myfolder):
        #     return HttpResponse("Upload failed")

        upload_file(myfolder)

        # result = LCA.contentAnalysis(text)

        return render(request, "conflict.html", {'result': str(myfolder),
                                                   'hidden': ""})
    else:
        # ctx['hidden'] = "hidden"
        return render(request, "conflict.html", {'hidden': "Hidden"})