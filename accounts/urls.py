from django.urls import path
from django.contrib.auth.views import LoginView
from .views import register_view, logout_view, profile_view


urlpatterns = [

    path(
        'register/',
        register_view,
        name='register'
    ),

    path(
        'login/',
        LoginView.as_view(
            template_name='accounts/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        logout_view,
        name='logout'
    ),

    path(
        'profile/',
        profile_view,
        name='profile'
    ),
]