from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def funtest(request):
    return render(request, 'CAPAPPv1/index.html')

def aboutfun(request):
    return render(request, 'CAPAPPv1/about.html')

def contactfun(request):
    return render(request, 'CAPAPPv1/contact.html')

def loginfun(request):
    return render(request, 'registration/login.html')

def homefun(request):
    return render(request, 'CAPAPPv1/ALog/home.html')