from django.shortcuts import render
from library.navigation import GetNavigationLinks
from library.errorLog import get_logger
logger = get_logger(__name__)


def index(request):
    nav_urls = GetNavigationLinks(request)
    template_name = "welcome/index.html"
    logger.info('rendering Welcome Index from {}'.format(template_name))
    
    return render(
        request, 
        template_name, 
        nav_urls)