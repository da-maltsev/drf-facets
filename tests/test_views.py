"""
Tests for DRF Facets views.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from drf_facets.models import ExampleModel


class ExampleModelViewSetTestCase(TestCase):
    """Test cases for ExampleModelViewSet."""
    
    def setUp(self):
        """Set up test data and client."""
        self.client = APIClient()
        
        # Create test examples
        self.example1 = ExampleModel.objects.create(
            name="Active Example",
            description="An active example",
            is_active=True,
        )
        self.example2 = ExampleModel.objects.create(
            name="Inactive Example",
            description="An inactive example",
            is_active=False,
        )
        self.example3 = ExampleModel.objects.create(
            name="Another Active Example",
            description="Another active example",
            is_active=True,
        )
    
    def test_list_examples(self):
        """Test listing all examples."""
        url = reverse("example-list")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)
        
        # Check that results are ordered by created_at descending
        names = [item["name"] for item in response.data["results"]]
        self.assertEqual(names[0], "Another Active Example")
        self.assertEqual(names[1], "Inactive Example")
        self.assertEqual(names[2], "Active Example")
    
    def test_retrieve_example(self):
        """Test retrieving a single example."""
        url = reverse("example-detail", args=[self.example1.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Active Example")
        self.assertEqual(response.data["description"], "An active example")
        self.assertTrue(response.data["is_active"])
    
    def test_create_example(self):
        """Test creating a new example."""
        url = reverse("example-list")
        data = {
            "name": "New Example",
            "description": "A new example",
            "is_active": True,
        }
        response = self.client.post(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Example")
        self.assertEqual(response.data["description"], "A new example")
        self.assertTrue(response.data["is_active"])
        
        # Check that the example was actually created
        self.assertTrue(ExampleModel.objects.filter(name="New Example").exists())
    
    def test_update_example(self):
        """Test updating an existing example."""
        url = reverse("example-detail", args=[self.example1.id])
        data = {
            "name": "Updated Example",
            "description": "An updated example",
            "is_active": False,
        }
        response = self.client.put(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Example")
        self.assertEqual(response.data["description"], "An updated example")
        self.assertFalse(response.data["is_active"])
        
        # Check that the example was actually updated
        self.example1.refresh_from_db()
        self.assertEqual(self.example1.name, "Updated Example")
    
    def test_partial_update_example(self):
        """Test partially updating an existing example."""
        url = reverse("example-detail", args=[self.example1.id])
        data = {"name": "Partially Updated Example"}
        response = self.client.patch(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Partially Updated Example")
        self.assertEqual(response.data["description"], "An active example")  # Unchanged
        self.assertTrue(response.data["is_active"])  # Unchanged
    
    def test_delete_example(self):
        """Test deleting an example."""
        url = reverse("example-detail", args=[self.example1.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the example was actually deleted
        self.assertFalse(ExampleModel.objects.filter(id=self.example1.id).exists())
    
    def test_filter_by_active_status(self):
        """Test filtering examples by active status."""
        url = reverse("example-list")
        response = self.client.get(url, {"is_active": "true"})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        
        # Check that only active examples are returned
        for item in response.data["results"]:
            self.assertTrue(item["is_active"])
    
    def test_filter_by_name(self):
        """Test filtering examples by name."""
        url = reverse("example-list")
        response = self.client.get(url, {"name": "Active"})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        
        # Check that only examples with "Active" in the name are returned
        for item in response.data["results"]:
            self.assertIn("Active", item["name"])
    
    def test_active_action(self):
        """Test the active action endpoint."""
        url = reverse("example-active")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Check that only active examples are returned
        for item in response.data:
            self.assertTrue(item["is_active"])
    
    def test_toggle_active_action(self):
        """Test the toggle_active action endpoint."""
        url = reverse("example-toggle-active", args=[self.example1.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_active"])
        
        # Check that the example was actually updated
        self.example1.refresh_from_db()
        self.assertFalse(self.example1.is_active)
        
        # Toggle again
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_active"])
    
    def test_stats_action(self):
        """Test the stats action endpoint."""
        url = reverse("example-stats")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total"], 3)
        self.assertEqual(response.data["active"], 2)
        self.assertEqual(response.data["inactive"], 1)
    
    def test_validation_error(self):
        """Test that validation errors are properly handled."""
        url = reverse("example-list")
        data = {
            "name": "A",  # Too short
            "description": "A test example",
            "is_active": True,
        }
        response = self.client.post(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data) 