from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.


def links(request):
    return HttpResponse("links")