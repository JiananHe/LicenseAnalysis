from django.shortcuts import render
from . import testdb

# Create your views here.
def index(request):
    ctx = {}
    # testdb.testdb_insert()
    ctx['result'] = testdb.testdb_search('test')
    return render(request, "customization.html", ctx)
