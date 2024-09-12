# views.py
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from ..models import Category
from ..serializers import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            response_data = {
                'success': True,
                'message': 'Category created successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({
            'success': False,
            'message': 'Failed to create category',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = {
            'success': True,
            'message': 'Category retrieved successfully',
            'data': serializer.data
        }
        return Response(response_data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            response_data = {
                'success': True,
                'message': 'Category updated successfully',
                'data': serializer.data
            }
            return Response(response_data)
        return Response({
            'success': False,
            'message': 'Failed to update category',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response_data = {
            'success': True,
            'message': 'Category deleted successfully',
            'data': None  # No data to return after deletion
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = {
                'success': True,
                'message': 'Categories retrieved successfully',
                'data': serializer.data
            }
            return self.get_paginated_response(response_data)

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'success': True,
            'message': 'Categories retrieved successfully',
            'data': serializer.data
        }
        return Response(response_data)