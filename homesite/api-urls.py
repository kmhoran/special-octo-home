from django.urls import include, path

urlpatterns = [
    path('v1/lists/', include('lists.urls')),
    path('users/', include('homesiteusers.urls')),
]