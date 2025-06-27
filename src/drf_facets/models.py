"""
Models for DRF Facets package.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class ExampleModel(models.Model):
    """
    Example model for demonstration purposes.
    
    This model shows how to create models in a Django package.
    """
    
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("The name of the example item"),
    )
    
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("A detailed description of the example item"),
        blank=True,
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is active"),
        help_text=_("Whether this item is currently active"),
    )
    
    class Meta:
        verbose_name = _("Example Model")
        verbose_name_plural = _("Example Models")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["is_active", "created_at"]),
        ]
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f"<ExampleModel: {self.name}>" 