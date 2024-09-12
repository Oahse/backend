# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import Transaction, DeliveryTracker
from ..serializers import TransactionSerializer, DeliveryTrackerSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save()
            response_data = {
                'success': True,
                'message': 'Transaction created successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': 'Failed to create transaction',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = {
            'success': True,
            'message': 'Transaction retrieved successfully',
            'data': serializer.data
        }
        return Response(response_data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response_data = {
            'success': True,
            'message': 'Transaction deleted successfully',
            'data': None
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = {
                'success': True,
                'message': 'Transactions retrieved successfully',
                'data': serializer.data
            }
            return self.get_paginated_response(response_data)

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'success': True,
            'message': 'Transactions retrieved successfully',
            'data': serializer.data
        }
        return Response(response_data)

class DeliveryTrackerViewSet(viewsets.ModelViewSet):
    queryset = DeliveryTracker.objects.all()
    serializer_class = DeliveryTrackerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            delivery_tracker = serializer.save()
            response_data = {
                'success': True,
                'message': 'DeliveryTracker created successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': 'Failed to create DeliveryTracker',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = {
            'success': True,
            'message': 'DeliveryTracker retrieved successfully',
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
                'message': 'DeliveryTracker updated successfully',
                'data': serializer.data
            }
            return Response(response_data)
        return Response({
            'success': False,
            'message': 'Failed to update DeliveryTracker',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response_data = {
            'success': True,
            'message': 'DeliveryTracker deleted successfully',
            'data': None
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = {
                'success': True,
                'message': 'DeliveryTrackers retrieved successfully',
                'data': serializer.data
            }
            return self.get_paginated_response(response_data)

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'success': True,
            'message': 'DeliveryTrackers retrieved successfully',
            'data': serializer.data
        }
        return Response(response_data)