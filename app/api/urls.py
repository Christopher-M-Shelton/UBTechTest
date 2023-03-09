from django.urls import include, path
from rest_framework import routers
from django.contrib.auth import views as auth_views

from .views import register, profile


router = routers.DefaultRouter()

urlpatterns = [
    path("register/", register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="api/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", profile, name="profile"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
