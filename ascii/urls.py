from django.urls import path
from ascii.views import *

app_name = 'ascii'

urlpatterns = [
    path('',ascii, name='ascii'),
    #path('getGraph/',getGraph,name="getGraph"),

]