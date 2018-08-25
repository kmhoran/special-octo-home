from django.shortcuts import render

def index(request):
    nav = None
    return render(request, "welcome/index.html")