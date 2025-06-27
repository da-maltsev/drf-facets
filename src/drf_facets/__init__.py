"""
DRF Facets - A Django package template for DRF extensions and utilities.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

default_app_config = "drf_facets.apps.DrfFacetsConfig"

# Import main components for easy access
from drf_facets.apps import DrfFacetsConfig


__all__ = [
    "DrfFacetsConfig",
    "__author__",
    "__email__",
    "__version__",
]
