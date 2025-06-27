"""
Tests for DRF Facets models.
"""

import time

from django.test import TestCase
from django.utils import timezone

from drf_facets.models import ExampleModel


class ExampleModelTestCase(TestCase):
    """Test cases for ExampleModel."""

    def setUp(self) -> None:
        """Set up test data."""
        self.example = ExampleModel.objects.create(
            name="Test Example",
            description="A test example for testing purposes",
            is_active=True,
        )

    def test_example_model_creation(self) -> None:
        """Test that ExampleModel can be created."""
        assert self.example.name == "Test Example"
        assert self.example.description == "A test example for testing purposes"
        assert self.example.is_active
        assert self.example.created_at is not None
        assert self.example.updated_at is not None

    def test_example_model_str(self) -> None:
        """Test the string representation of ExampleModel."""
        assert str(self.example) == "Test Example"

    def test_example_model_repr(self) -> None:
        """Test the repr representation of ExampleModel."""
        expected_repr = f"<ExampleModel: {self.example.name}>"
        assert repr(self.example) == expected_repr

    def test_example_model_ordering(self) -> None:
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
        assert examples[0] == second_example
        assert examples[1] == self.example

    def test_example_model_defaults(self) -> None:
        """Test ExampleModel default values."""
        example = ExampleModel.objects.create(name="Default Test")

        assert example.name == "Default Test"
        assert example.description == ""  # blank=True
        assert example.is_active  # default=True
        assert example.created_at is not None
        assert example.updated_at is not None

    def test_example_model_auto_timestamps(self) -> None:
        """Test that timestamps are automatically set."""
        before_creation = timezone.now()

        example = ExampleModel.objects.create(name="Timestamp Test")

        after_creation = timezone.now()

        assert example.created_at >= before_creation
        assert example.created_at <= after_creation
        assert example.created_at == example.updated_at

    def test_example_model_update_timestamp(self) -> None:
        """Test that updated_at is updated when the model is saved."""
        original_updated_at = self.example.updated_at

        # Wait a bit to ensure timestamp difference
        time.sleep(0.001)

        # Update the model
        self.example.name = "Updated Name"
        self.example.save()

        assert self.example.updated_at > original_updated_at
