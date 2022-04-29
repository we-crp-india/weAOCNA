from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.home,name = 'login'),
    path('dashboard/',views.dash,name = 'dashboard'),
    path('logout/',views.logoutUser,name = 'logoutUser'),
    path('update/',views.updateCase,name = 'update'),
    path('error/',views.ErrorFound,name = 'error'),
    path('details/',views.Details,name = 'details'),
]