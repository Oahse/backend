from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q
from django.db.models.functions import Lower
from django.db.models.functions import Cast
from django.db.models import TextField
from django.db import connection
from collections import defaultdict
from ..models import Product
from ..serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            response_data = {
                'success': True,
                'message': 'Product created successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({
            'success': False,
            'message': 'Failed to create product',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = {
            'success': True,
            'message': 'Product retrieved successfully',
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
                'message': 'Product updated successfully',
                'data': serializer.data
            }
            return Response(response_data)
        return Response({
            'success': False,
            'message': 'Failed to update product',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response_data = {
            'success': True,
            'message': 'Product deleted successfully',
            'data': None  # No data to return after deletion
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)


    def filter_products(self, request, queryset):
        # Get parameters from the request body
        search_query = request.data.get('search', None)
        price_range = request.data.get('price_range', None)  # Expecting 'min,max'
        category_id = request.data.get('category', None)
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)

        queryset = Product.objects.all()

        # Search by name or description
        if search_query:
            # Handle JSON search compatibility
            if connection.vendor == 'postgresql':
                queryset = queryset.filter(
                    Q(name__icontains=search_query) | 
                    Q(description__icontains=search_query) |
                    Q(address__icontains=search_query)| 
                    Q(hashtags__contains=[search_query])
                )
            else:
                queryset = queryset.annotate(
                    hashtags_text=Cast('hashtags', TextField()),
                    lower_name=Lower('name'),
                    lower_description=Lower('description'),
                    lower_address=Lower('address')
                ).filter(
                    Q(lower_name__icontains=search_query) | 
                    Q(lower_description__icontains=search_query) |
                    Q(lower_address__icontains=search_query)| 
                    Q(hashtags_text__icontains=search_query)
                )

        # Filter by price range
        if price_range:
            min_price, max_price = map(float, price_range.split(','))
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        # Filter by category
        if category_id:
            queryset = queryset.filter(category__id=category_id)

        # Filter by date range
        if start_date and end_date:
            queryset = queryset.filter(createdat__range=[start_date, end_date])

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Grouping products by category
        grouped_data = defaultdict(list)

        for product in self.filter_products(request, queryset):
            category_name = product.category.name if product.category else "Uncategorized"
            grouped_data[category_name].append(product)

        # Transform the data into the desired output format
        response_data = []

        for category, items in grouped_data.items():
            # Collect all unique hashtags for this category
            hashtags = set()
            for item in items:
                hashtags.update(item.hashtags)

            # Append the data in the desired format
            response_data.append({
                'category': category,
                'sections': list(hashtags),  # Convert set of hashtags to a list
                'items': [ProductSerializer(item).data for item in items]
            })

        # Return the response
        return Response({
            'success': True,
            'message': 'Products retrieved successfully',
            'data': response_data
        })