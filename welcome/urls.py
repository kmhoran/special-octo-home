from django.urls import include, path
from welcome import views

urlpatterns = [
    path('', views.index, name='main-index'),
]