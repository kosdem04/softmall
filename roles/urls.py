from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("add_group", views.UserGroupAdd.as_view(), name="add_group"),
    path("add_role", views.RoleAdd.as_view(), name="add_role"),
    path("add_user_role", views.UserRoleAdd.as_view(), name="add_user_role"),
    path("add_function", views.FunctionAdd.as_view(), name="add_function"),
    path("add_role_function", views.RoleFunctionAdd.as_view(), name="add_role_function"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
