from django.urls import path
from account.views import *
app_name = "account"

urlpatterns = [
    path("login/", user_login, name="login"),
    path("register/",register, name="register"),
    path("logout/", user_logout, name="logout"),
]
