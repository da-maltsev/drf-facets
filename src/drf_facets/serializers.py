"""
Serializers for DRF Facets package.
"""

from rest_framework import serializers

from .models import ExampleModel


class ExampleModelSerializer(serializers.ModelSerializer):
    """
    Serializer for ExampleModel.
    
    Provides full CRUD operations for the ExampleModel.
    """
    
    class Meta:
        model = ExampleModel
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
            "is_active",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
    
    def validate_name(self, value: str) -> str:
        """
        Validate the name field.
        
        Args:
            value: The name value to validate
            
        Returns:
            The validated name
            
        Raises:
            serializers.ValidationError: If the name is invalid
        """
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Name must be at least 2 characters long."
            )
        return value.strip()


class ExampleModelListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing ExampleModel instances.
    
    Used for list views where full details are not needed.
    """
    
    class Meta:
        model = ExampleModel
        fields = ["id", "name", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"] 