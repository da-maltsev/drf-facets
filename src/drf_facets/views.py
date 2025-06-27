"""
Views for DRF Facets package.
"""

from typing import Any

from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from drf_facets.models import ExampleModel
from drf_facets.serializers import ExampleModelListSerializer, ExampleModelSerializer


class ExampleModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ExampleModel.

    Provides full CRUD operations for ExampleModel instances.
    """

    queryset = ExampleModel.objects.all()
    serializer_class = ExampleModelSerializer

    def get_serializer_class(self) -> type[serializers.ModelSerializer]:
        """
        Return appropriate serializer class based on the action.

        Returns:
            The serializer class to use

        """
        if self.action == "list":
            return ExampleModelListSerializer
        return ExampleModelSerializer

    def get_queryset(self) -> Any:
        """
        Filter queryset based on query parameters.

        Returns:
            Filtered queryset

        """
        queryset = ExampleModel.objects.all()

        # Filter by active status
        is_active = self.request.query_params.get("is_active", None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == "true")

        # Filter by name (case-insensitive contains)
        name = self.request.query_params.get("name", None)
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    @action(detail=False, methods=["get"])
    def active(self, request: Request) -> Response:
        """
        Get only active ExampleModel instances.

        Returns:
            Response with active instances

        """
        active_items = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(active_items, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def toggle_active(self, request: Request, pk: int | None = None) -> Response:
        """
        Toggle the active status of an ExampleModel instance.

        Args:
            request: The request object
            pk: The primary key of the instance

        Returns:
            Response with updated instance data

        """
        instance = self.get_object()
        instance.is_active = not instance.is_active
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def stats(self, request: Request) -> Response:
        """
        Get statistics about ExampleModel instances.

        Returns:
            Response with statistics

        """
        total_count = ExampleModel.objects.count()
        active_count = ExampleModel.objects.filter(is_active=True).count()
        inactive_count = total_count - active_count

        return Response(
            {
                "total": total_count,
                "active": active_count,
                "inactive": inactive_count,
            }
        )
