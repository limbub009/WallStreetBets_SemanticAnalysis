# map urls to view functions
from django.http.response import StreamingHttpResponse
from django.urls import path
from . import views

#URL CONFIGURATION
urlpatterns = [
    path('', views.homepage, name = 'homepage'),
    path('rSA', views.redditSA , name = 'rsa'),
    path('tSA', views.twitterSA, name = 'tsa'),
    path('fc', views.fc, name = 'fc'),
    
]

