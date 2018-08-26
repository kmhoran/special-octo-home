from django.urls import reverse
from django.conf import settings

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

    return {
        'home': home_url,
        'login': login_url,
        'logout': logout_url,
        'debug': debug
    }