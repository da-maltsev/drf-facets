"""
Tests for DRF Facets serializers.
"""

from django.test import TestCase

from drf_facets.models import ExampleModel
from drf_facets.serializers import ExampleModelListSerializer, ExampleModelSerializer


class ExampleModelSerializerTestCase(TestCase):
    """Test cases for ExampleModelSerializer."""

    def setUp(self) -> None:
        """Set up test data."""
        self.example_data = {
            "name": "Test Example",
            "description": "A test example for testing purposes",
            "is_active": True,
        }
        self.example = ExampleModel.objects.create(**self.example_data)

    def test_serializer_valid_data(self) -> None:
        """Test that serializer accepts valid data."""
        serializer = ExampleModelSerializer(data=self.example_data)
        assert serializer.is_valid()

    def test_serializer_invalid_name_too_short(self) -> None:
        """Test that serializer rejects names that are too short."""
        invalid_data = self.example_data.copy()
        invalid_data["name"] = "A"  # Too short

        serializer = ExampleModelSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_serializer_invalid_name_whitespace_only(self) -> None:
        """Test that serializer rejects names that are only whitespace."""
        invalid_data = self.example_data.copy()
        invalid_data["name"] = "   "  # Only whitespace

        serializer = ExampleModelSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_serializer_name_stripping(self) -> None:
        """Test that serializer strips whitespace from names."""
        data_with_whitespace = self.example_data.copy()
        data_with_whitespace["name"] = "  Test Example  "

        serializer = ExampleModelSerializer(data=data_with_whitespace)
        assert serializer.is_valid()
        assert serializer.validated_data["name"] == "Test Example"

    def test_serializer_serialization(self) -> None:
        """Test that serializer correctly serializes model instances."""
        serializer = ExampleModelSerializer(self.example)
        data = serializer.data

        assert data["name"] == self.example.name
        assert data["description"] == self.example.description
        assert data["is_active"] == self.example.is_active
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_serializer_read_only_fields(self) -> None:
        """Test that read-only fields are not included in validation."""
        data_with_readonly = self.example_data.copy()
        data_with_readonly["id"] = 999
        data_with_readonly["created_at"] = "2024-01-01T00:00:00Z"

        serializer = ExampleModelSerializer(data=data_with_readonly)
        assert serializer.is_valid()

        # Read-only fields should be ignored during validation
        assert "id" not in serializer.validated_data
        assert "created_at" not in serializer.validated_data


class ExampleModelListSerializerTestCase(TestCase):
    """Test cases for ExampleModelListSerializer."""

    def setUp(self) -> None:
        """Set up test data."""
        self.example = ExampleModel.objects.create(
            name="Test Example",
            description="A test example for testing purposes",
            is_active=True,
        )

    def test_list_serializer_fields(self) -> None:
        """Test that list serializer includes only specific fields."""
        serializer = ExampleModelListSerializer(self.example)
        data = serializer.data

        expected_fields = {"id", "name", "is_active", "created_at"}
        assert set(data.keys()) == expected_fields

        # Check that description and updated_at are not included
        assert "description" not in data
        assert "updated_at" not in data

    def test_list_serializer_data(self) -> None:
        """Test that list serializer contains correct data."""
        serializer = ExampleModelListSerializer(self.example)
        data = serializer.data

        assert data["id"] == self.example.id
        assert data["name"] == self.example.name
        assert data["is_active"] == self.example.is_active
        assert data["created_at"] is not None

    def test_list_serializer_read_only_fields(self) -> None:
        """Test that list serializer read-only fields are handled correctly."""
        data = {
            "name": "New Example",
            "is_active": False,
        }

        serializer = ExampleModelListSerializer(data=data)
        assert serializer.is_valid()

        # Read-only fields should not be in validated_data
        assert "id" not in serializer.validated_data
        assert "created_at" not in serializer.validated_data
