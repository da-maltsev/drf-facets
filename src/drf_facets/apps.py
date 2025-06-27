"""
Django app configuration for DRF Facets.
"""

from django.apps import AppConfig


class DrfFacetsConfig(AppConfig):
    """Configuration for the DRF Facets app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "drf_facets"
    verbose_name = "DRF Facets"

    def ready(self) -> None:
        """Initialize the app when Django starts."""
        # Import signals or other initialization code here
