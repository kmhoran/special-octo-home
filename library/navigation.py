from django.urls import reverse
from django.conf import settings
from library.errorLog import get_logger
logger = get_logger(__name__)

def GetNavigationLinks(request):
    home_url = reverse("main-index")
    login_url = ''
    logout_url = ''
    debug = False

    if request.user.is_authenticated:
        logout_url = reverse('logout')
    else:
        login_url = reverse('login')

    debug = settings.DEBUG
    nav_dict = {
        'home': home_url,
        'login': login_url,
        'logout': logout_url,
        'debug': debug
    }
    logger_string = 'renduring site-navigation dict : {}'.format(str(nav_dict).replace(',','..')) 
    logger.info(logger_string)
    
    return nav_dict 