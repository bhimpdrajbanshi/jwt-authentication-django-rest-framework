
from django.urls import path
from .views import UserLoginAPI, UserRegistrationAPI

urlpatterns = [
    path('login/', UserLoginAPI.as_view(), name='user-login'),
    path('user/regisration/', UserRegistrationAPI.as_view(), name='user-regisration'),
]
