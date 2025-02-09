from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("add_setting_dict", views.AddSettingDict.as_view(), name="add_setting_dict"),
    path("add_setting", views.AddSetting.as_view(), name="add_setting"),
    path("show_settings", views.show_settings, name="show_settings"),
    path("edit_setting/<int:setting_pk>", views.EditSetting.as_view(), name="edit_setting"),
    path("delete_setting/<int:setting_pk>", views.delete_setting, name="delete_setting"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
