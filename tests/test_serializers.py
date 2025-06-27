"""
Tests for DRF Facets serializers.
"""

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from drf_facets.models import ExampleModel
from drf_facets.serializers import ExampleModelSerializer, ExampleModelListSerializer


class ExampleModelSerializerTestCase(TestCase):
    """Test cases for ExampleModelSerializer."""
    
    def setUp(self):
        """Set up test data."""
        self.example_data = {
            "name": "Test Example",
            "description": "A test example for testing purposes",
            "is_active": True,
        }
        self.example = ExampleModel.objects.create(**self.example_data)
    
    def test_serializer_valid_data(self):
        """Test that serializer accepts valid data."""
        serializer = ExampleModelSerializer(data=self.example_data)
        self.assertTrue(serializer.is_valid())
    
    def test_serializer_invalid_name_too_short(self):
        """Test that serializer rejects names that are too short."""
        invalid_data = self.example_data.copy()
        invalid_data["name"] = "A"  # Too short
        
        serializer = ExampleModelSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
    
    def test_serializer_invalid_name_whitespace_only(self):
        """Test that serializer rejects names that are only whitespace."""
        invalid_data = self.example_data.copy()
        invalid_data["name"] = "   "  # Only whitespace
        
        serializer = ExampleModelSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
    
    def test_serializer_name_stripping(self):
        """Test that serializer strips whitespace from names."""
        data_with_whitespace = self.example_data.copy()
        data_with_whitespace["name"] = "  Test Example  "
        
        serializer = ExampleModelSerializer(data=data_with_whitespace)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], "Test Example")
    
    def test_serializer_serialization(self):
        """Test that serializer correctly serializes model instances."""
        serializer = ExampleModelSerializer(self.example)
        data = serializer.data
        
        self.assertEqual(data["name"], self.example.name)
        self.assertEqual(data["description"], self.example.description)
        self.assertEqual(data["is_active"], self.example.is_active)
        self.assertIn("id", data)
        self.assertIn("created_at", data)
        self.assertIn("updated_at", data)
    
    def test_serializer_read_only_fields(self):
        """Test that read-only fields are not included in validation."""
        data_with_readonly = self.example_data.copy()
        data_with_readonly["id"] = 999
        data_with_readonly["created_at"] = "2024-01-01T00:00:00Z"
        
        serializer = ExampleModelSerializer(data=data_with_readonly)
        self.assertTrue(serializer.is_valid())
        
        # Read-only fields should be ignored during validation
        self.assertNotIn("id", serializer.validated_data)
        self.assertNotIn("created_at", serializer.validated_data)


class ExampleModelListSerializerTestCase(TestCase):
    """Test cases for ExampleModelListSerializer."""
    
    def setUp(self):
        """Set up test data."""
        self.example = ExampleModel.objects.create(
            name="Test Example",
            description="A test example for testing purposes",
            is_active=True,
        )
    
    def test_list_serializer_fields(self):
        """Test that list serializer includes only specific fields."""
        serializer = ExampleModelListSerializer(self.example)
        data = serializer.data
        
        expected_fields = {"id", "name", "is_active", "created_at"}
        self.assertEqual(set(data.keys()), expected_fields)
        
        # Check that description and updated_at are not included
        self.assertNotIn("description", data)
        self.assertNotIn("updated_at", data)
    
    def test_list_serializer_data(self):
        """Test that list serializer contains correct data."""
        serializer = ExampleModelListSerializer(self.example)
        data = serializer.data
        
        self.assertEqual(data["id"], self.example.id)
        self.assertEqual(data["name"], self.example.name)
        self.assertEqual(data["is_active"], self.example.is_active)
        self.assertIsNotNone(data["created_at"])
    
    def test_list_serializer_read_only_fields(self):
        """Test that list serializer read-only fields are handled correctly."""
        data = {
            "name": "New Example",
            "is_active": False,
        }
        
        serializer = ExampleModelListSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        # Read-only fields should not be in validated_data
        self.assertNotIn("id", serializer.validated_data)
        self.assertNotIn("created_at", serializer.validated_data) 