from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import Job, Service, Review, Comments
from ..serializers import JobSerializer, ServiceSerializer, ReviewSerializer, CommentsSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            job = serializer.save()
            response_data = {
                'success': True,
                'message': 'Job created successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': 'Failed to create job',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = {
            'success': True,
            'message': 'Job retrieved successfully',
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
                'message': 'Job updated successfully',
                'data': serializer.data
            }
            return Response(response_data)
        return Response({
            'success': False,
            'message': 'Failed to update job',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response_data = {
            'success': True,
            'message': 'Job deleted successfully',
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
                'message': 'Jobs retrieved successfully',
                'data': serializer.data
            }
            return self.get_paginated_response(response_data)

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'success': True,
            'message': 'Jobs retrieved successfully',
            'data': serializer.data
        }
        return Response(response_data)

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            service = serializer.save()
            response_data = {
                'success': True,
                'message': 'Service created successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': 'Failed to create service',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = {
            'success': True,
            'message': 'Service retrieved successfully',
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
                'message': 'Service updated successfully',
                'data': serializer.data
            }
            return Response(response_data)
        return Response({
            'success': False,
            'message': 'Failed to update service',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response_data = {
            'success': True,
            'message': 'Service deleted successfully',
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
                'message': 'Services retrieved successfully',
                'data': serializer.data
            }
            return self.get_paginated_response(response_data)

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'success': True,
            'message': 'Services retrieved successfully',
            'data': serializer.data
        }
        return Response(response_data)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save()
            response_data = {
                'success': True,
                'message': 'Review created successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': 'Failed to create review',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = {
            'success': True,
            'message': 'Review retrieved successfully',
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
                'message': 'Review updated successfully',
                'data': serializer.data
            }
            return Response(response_data)
        return Response({
            'success': False,
            'message': 'Failed to update review',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response_data = {
            'success': True,
            'message': 'Review deleted successfully',
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
                'message': 'Reviews retrieved successfully',
                'data': serializer.data
            }
            return self.get_paginated_response(response_data)

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'success': True,
            'message': 'Reviews retrieved successfully',
            'data': serializer.data
        }
        return Response(response_data)

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save()
            response_data = {
                'success': True,
                'message': 'Comment created successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': 'Failed to create comment',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            response_data = {
                'success': True,
                'message': 'Comment updated successfully',
                'data': serializer.data
            }
            return Response(response_data)
        return Response({
            'success': False,
            'message': 'Failed to update comment',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = {
            'success': True,
            'message': 'Comment retrieved successfully',
            'data': serializer.data
        }
        return Response(response_data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response_data = {
            'success': True,
            'message': 'Comment deleted successfully',
            'data': None
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)
    def list_by_reviewid(self, request, reviewid=None):
        if reviewid is None:
            return Response({
                'success': False,
                'message': 'Review ID is required to retrieve comments by reviewid',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        comments = Comments.objects.filter(reviewid=reviewid)
        serializer = self.get_serializer(comments, many=True)
        response_data = {
            'success': True,
            'message': f'Comments for review ID {reviewid} retrieved successfully',
            'data': serializer.data
        }
        return Response(response_data)

    # Override the list method to handle both standard list and list_by_reviewid
    def list(self, request, *args, **kwargs):
        if 'reviewid' in request.query_params:
            return self.list_by_reviewid(request, reviewid=request.query_params['reviewid'])
        
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = {
                'success': True,
                'message': 'Comments retrieved successfully',
                'data': serializer.data
            }
            return self.get_paginated_response(response_data)

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'success': True,
            'message': 'Comments retrieved successfully',
            'data': serializer.data
        }
        return Response(response_data)
    