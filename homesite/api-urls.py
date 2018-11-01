from django.urls import include, path

urlpatterns = [
    path('v1/lists/', include('lists.urls')),
    path('v1/users/', include('homesiteusers.urls')),
]