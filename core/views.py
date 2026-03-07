from django.shortcuts import render
from django.http import HttpResponse

def accueil(request):
    return HttpResponse("<h1>Programme facturation  Jah.Abdeelfattah</h1>")
# Create your views here.
