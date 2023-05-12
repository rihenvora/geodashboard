from django.urls import path
from members.views import *
'''from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('download/',views.download_file,name='download/')
]'''
app_name = 'members'

urlpatterns = [
    path('', index, name='index'),
    #path('download/',download_file, name='download')
    #path('testFunc/', testFunc, name='testFunc'),
    path('getUserData/',getUserData, name='getUserData'),
    path('getInterpretedCpt/',getInterpretedCpt, name='getInterpretedCpt'),
    path('getLVAN/',getLVAN, name='getLVAN'),
]