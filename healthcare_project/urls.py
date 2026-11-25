"""
healthcare_project/urls.py  —  Root URL configuration.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def api_root(request):
    """
    Healthcare Management System API Directory
    """
    return Response({
        "project": "Healthcare Management Backend API",
        "version": "1.0.0",
        "status": "online",
        "documentation": "https://github.com/your-org/healthcare-api",
        "endpoints": {
            "authentication": {
                "register": request.build_absolute_uri("api/auth/register/"),
                "login": request.build_absolute_uri("api/auth/login/"),
                "token_refresh": request.build_absolute_uri("api/auth/token/refresh/"),
            },
            "patients": {
                "list_and_create": request.build_absolute_uri("api/patients/"),
                "detail_update_delete": request.build_absolute_uri("api/patients/<id>/"),
            },
            "doctors": {
                "list_and_create": request.build_absolute_uri("api/doctors/"),
                "detail_update_delete": request.build_absolute_uri("api/doctors/<id>/"),
            },
            "patient_doctor_mappings": {
                "list_and_create": request.build_absolute_uri("api/mappings/"),
                "by_patient": request.build_absolute_uri("api/mappings/<patient_id>/"),
                "delete": request.build_absolute_uri("api/mappings/delete/<id>/"),
            },
            "admin_panel": request.build_absolute_uri("admin/"),
        }
    })


urlpatterns = [
    path("", api_root, name="api-root"),
    path("api/", api_root, name="api-index"),
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/patients/", include("patients.urls")),
    path("api/doctors/", include("doctors.urls")),
    path("api/mappings/", include("mappings.urls")),
]
