from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('home/',views.home),
    path('team/',views.team),
    path('locateus/',views.locateus),
    path('about/',views.about),
    path('register/',views.register),
    path('adopt/',views.adopt),
]