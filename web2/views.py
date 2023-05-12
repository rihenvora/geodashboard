from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    #print("RIHEN")
    return render(request,'index-home.html')