"""
Tests for DRF Facets models.
"""

import pytest
from django.test import TestCase
from django.utils import timezone

from drf_facets.models import ExampleModel


class ExampleModelTestCase(TestCase):
    """Test cases for ExampleModel."""
    
    def setUp(self):
        """Set up test data."""
        self.example = ExampleModel.objects.create(
            name="Test Example",
            description="A test example for testing purposes",
            is_active=True,
        )
    
    def test_example_model_creation(self):
        """Test that ExampleModel can be created."""
        self.assertEqual(self.example.name, "Test Example")
        self.assertEqual(self.example.description, "A test example for testing purposes")
        self.assertTrue(self.example.is_active)
        self.assertIsNotNone(self.example.created_at)
        self.assertIsNotNone(self.example.updated_at)
    
    def test_example_model_str(self):
        """Test the string representation of ExampleModel."""
        self.assertEqual(str(self.example), "Test Example")
    
    def test_example_model_repr(self):
        """Test the repr representation of ExampleModel."""
        expected_repr = f"<ExampleModel: {self.example.name}>"
        self.assertEqual(repr(self.example), expected_repr)
    
    def test_example_model_ordering(self):
        """Test that ExampleModel instances are ordered by created_at descending."""
        # Create another example
        second_example = ExampleModel.objects.create(
            name="Second Example",
            description="Another test example",
            is_active=False,
        )
        
        # Get all examples
        examples = list(ExampleModel.objects.all())
        
        # Check ordering (newest first)
        self.assertEqual(examples[0], second_example)
        self.assertEqual(examples[1], self.example)
    
    def test_example_model_defaults(self):
        """Test ExampleModel default values."""
        example = ExampleModel.objects.create(name="Default Test")
        
        self.assertEqual(example.name, "Default Test")
        self.assertEqual(example.description, "")  # blank=True
        self.assertTrue(example.is_active)  # default=True
        self.assertIsNotNone(example.created_at)
        self.assertIsNotNone(example.updated_at)
    
    def test_example_model_auto_timestamps(self):
        """Test that timestamps are automatically set."""
        before_creation = timezone.now()
        
        example = ExampleModel.objects.create(name="Timestamp Test")
        
        after_creation = timezone.now()
        
        self.assertGreaterEqual(example.created_at, before_creation)
        self.assertLessEqual(example.created_at, after_creation)
        self.assertEqual(example.created_at, example.updated_at)
    
    def test_example_model_update_timestamp(self):
        """Test that updated_at is updated when the model is saved."""
        original_updated_at = self.example.updated_at
        
        # Wait a bit to ensure timestamp difference
        import time
        time.sleep(0.001)
        
        # Update the model
        self.example.name = "Updated Name"
        self.example.save()
        
        self.assertGreater(self.example.updated_at, original_updated_at) 