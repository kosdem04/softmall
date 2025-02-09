from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.main, name="main"),
    path("login/", views.Auth.as_view(), name="login"),
    path("user_reg/", views.UserReg.as_view(), name="user_reg"),
    path("profile/", views.profile, name="profile"),
    path("logout", views.logout_view, name='logout'),
    path("admin_panel", views.admin_panel, name='admin_panel'),
    path("change_password", views.ChangePassword.as_view(), name='change_password'),
    path("change_password_complete", views.change_password_complete, name='change_password_complete'),
    path("send_mail", views.SendMail.as_view(), name="send_mail"),
    path("support", views.support, name="support"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

