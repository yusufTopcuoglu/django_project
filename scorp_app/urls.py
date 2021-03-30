from django.urls import path

from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.index, name='index'),
    path('user/<str:username>', views.get_user, name='get_user'),
    path('users', views.get_users, name='get_users'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('login', obtain_auth_token, name="login"),
]
