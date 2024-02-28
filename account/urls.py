from django.urls import path
from django.contrib.auth import views
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout'),
]
