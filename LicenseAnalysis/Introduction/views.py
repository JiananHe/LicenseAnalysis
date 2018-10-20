from django.shortcuts import render
from django.http import HttpResponse
import sys
sys.path.append("..")
import LicenseModel.models as LM


# Create your views here.
def index(request):
    search_text = ''
    if request.POST:  # receive search text from search box
        search_text = request.POST['search-text']

    search_result = LM.searchLicense(search_text)

    # return as dict to facilitate parsing in html to generate dynamic page
    ctx = {'lst': search_result}
    return render(request, "introduction.html", ctx)


def full_content(request):
    # parse the license name in request url
    license_abbr = str(request.path).split("/")[-1]

    ctx = LM.searchContent(license_abbr)
    return render(request, "introduction-full.html", ctx)
