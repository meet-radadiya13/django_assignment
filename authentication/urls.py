from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from authentication import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.render_login, name="login"),
    path("save_user/", views.save_user, name="save_user"),
    path("validate_user/", views.validate_user, name="validate_user"),
    path("profile/", views.render_profile, name="profile"),
    path("edit_user/", views.edit_user, name="edit_user"),
    path("edit_password/", views.edit_password, name="edit_password"),
    path(
        "logout/",
        LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL),
        name="logout",
    ),
]
