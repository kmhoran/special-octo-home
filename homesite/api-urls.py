from django.urls import include, path

urlpatterns = [
    path('lists/', include('lists.urls')),
    path('users/', include('homesiteusers.urls')),
]