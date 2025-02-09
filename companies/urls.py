from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("add", views.AddCompany.as_view(), name="add_company"),
    path("info/<int:company_pk>", views.company_info, name="company_info"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
