from django.urls import path, re_path
from django.shortcuts import render

def frontend_spa(request):
    print("frontend_spa")
    return render(request, 'frontend/index.html')

urlpatterns = [
    re_path('.*', frontend_spa, name='index-reverse-proxy'),
    path('', frontend_spa, name='index'),
]