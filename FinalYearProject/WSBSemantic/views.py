from django.shortcuts import render
from django.http import HttpResponse
from WSBSemantic.utils import SARedditOut

# Create your views here.
# request -> response
# request handler
# action
# something that a user sees




#map view to URL
def homepage(request):
    return render(request, 'home.html')


def redditSA(request):
    if request.method == 'POST' and 'run_script' in request.POST:
        print (SARedditOut())
    return render(request, 'redditSA.html')


def twitterSA(request):
    return render(request, 'twitterSA.html')


def fc(request):
    return render(request, 'fc.html')

