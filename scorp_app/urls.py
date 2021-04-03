from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user', views.get_or_update_user, name='get_or_update_user'),
    path('users', views.get_users, name='get_users'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('login', obtain_auth_token, name="login"),
    path('follow/<str:followee_name>', views.follow, name="follow"),
    path('followers', views.followers, name="followers"),
    path('followees', views.followees, name="followees"),
    path('post', views.post, name="post"),
]
