"""
URL configuration for DRF Facets package.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ExampleModelViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r"examples", ExampleModelViewSet, basename="example")

app_name = "drf_facets"

urlpatterns = [
    # API endpoints
    path("api/", include(router.urls)),
    
    # Include DRF's browsable API authentication URLs
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
] 