from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def respuesta(request):
    return HttpResponse("Hola")