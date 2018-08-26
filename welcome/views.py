from django.shortcuts import render
from library.navigation import GetNavigationLinks

def index(request):
    nav_urls = GetNavigationLinks(request)

    return render(
        request, 
        "welcome/index.html", 
        nav_urls)