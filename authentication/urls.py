from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import TemplateView

from authentication import views

urlpatterns = [
    path(
        "",
        login_required(TemplateView.as_view(template_name="root/home.html")),
        name="home",
    ),
    path(
        "login/",
        TemplateView.as_view(template_name="user/login.html"),
        name="login",
    ),
    path("save_user/", views.save_user, name="save_user"),
    path("validate_user/", views.validate_user, name="validate_user"),
    path(
        "profile/",
        login_required(TemplateView.as_view(template_name="user/profile.html")),
        name="profile",
    ),
    path("edit_user/", views.edit_user, name="edit_user"),
    path("edit_password/", views.edit_password, name="edit_password"),
    path(
        "logout/",
        LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL),
        name="logout",
    ),
]
