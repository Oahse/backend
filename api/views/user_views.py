from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status, viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from ..utils import Util

from ..models import User, Profession
from ..serializers import (
    UserSerializer, UserLoginSerializer,BusinessSerializer,DelivererSerializer, DistributorSerializer,ProfessionSerializer,TradePersonSerializer
)



def send_verification_email(request, user, email, type, subject):
    token = default_token_generator.make_token(user)
    websitetype = 'noreply@yourwebsite.com'
    Util.send_email(request, user, email, token, websitetype, type, subject)

def filter_queryset(filter, serializer):
    # Define the fields you want to include in the print
        if filter == 'is_tradeperson':
            fields_to_print = ['id',"title", 'first_name',"last_name","phonenumber",'nin',"passport",'image', 'email','address','is_active','verified','verifiedAt','avgratings','is_tradeperson','professionname','regulations','date_joined','updatedAt','last_login','last_login_location']
        elif filter == 'is_business':
            fields_to_print = ['id',"phonenumber",'image', 'email','address','is_active','verified','verifiedAt','avgratings','is_business','businessname','cac',"websiteurl",'date_joined','updatedAt','last_login','last_login_location']
        elif filter == 'is_distributor':
            fields_to_print = ['id',"phonenumber",'image', 'email','address','is_active','verified','verifiedAt','avgratings','is_distributor','distributorname','businessname',"websiteurl",'date_joined','updatedAt','last_login','last_login_location']
        elif filter == 'is_deliverer':
            fields_to_print = ['id',"phonenumber",'image', 'email','address','is_active','verified','verifiedAt','avgratings','is_deliverer','deliverername','cac',"websiteurl",'date_joined','updatedAt','last_login','last_login_location']
        elif filter =='is_superuser':
            fields_to_print = ['id',"title", 'first_name',"last_name","phonenumber",'nin',"passport",'image', 'email','address','is_active',"is_staff",'verified','verifiedAt','avgratings','is_superuser','date_joined','updatedAt','last_login','last_login_location']
        else:
            ##filter == 'is_client'
            fields_to_print = ['id',"title", 'first_name',"last_name","phonenumber",'nin',"passport",'image', 'email','address','is_active',"is_staff",'is_superuser','verified','verifiedAt','avgratings','date_joined','updatedAt','last_login','last_login_location']
        # Check if serializer.data is a dictionary (single object) or a list (queryset)
        if isinstance(serializer.data, dict):
            # Single object case
            filtered_data = {field: serializer.data[field] for field in fields_to_print if field in serializer.data}
        elif isinstance(serializer.data, list):
            # Multiple objects case
            filtered_data = [
                {field: item[field] for field in fields_to_print if field in item}
                for item in serializer.data
            ]
        else:
            filtered_data = {}
        return filtered_data

class BaseUserViewSet(viewsets.ModelViewSet):
    
    permission_classes = [AllowAny]

    def perform_create(self, request, serializer):
        data = request.data
        user = serializer.save(password=data['password'])
        send_verification_email(request, user, data.get('email'),'email_verification', 'Email Verification')
        refresh = RefreshToken.for_user(user)
        usertype = self.filterparam.replace('is_', '')
        return Response({
            'success': True,
            'message': f'{usertype} registered successfully',
            'userid': user.id,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        usertype = self.filterparam.replace('is_', '')
        if serializer.is_valid():
            return self.perform_create(request, serializer)
        return Response({'success': False, 'message': f'Failed to register {usertype}', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(user)
        filtered_data = filter_queryset(self.filterparam, serializer)
        usertype = self.filterparam.replace('is_', '')
        #print(filtered_data)
        return Response({'success': True, 'message': f'{usertype} details retrieved successfully', 'data': filtered_data})
    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        filtered_data = filter_queryset(self.filterparam, serializer)
        usertype = self.filterparam.replace('is_', '')
        #print(filtered_data)
        return Response({'success': True,'message': f'{usertype}s retrieved successfully',  'data': filtered_data})

    def update(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        usertype = self.filterparam.replace('is_', '')
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': f'{usertype} updated successfully', 'data': serializer.data})
        return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        usertype = self.filterparam.replace('is_', '')
        user.delete()
        return Response({'success': True, 'message': f'{usertype} deleted successfully','data': None}, status=status.HTTP_204_NO_CONTENT)

class CreateUserViewSet(BaseUserViewSet):
    queryset = User.objects.filter(is_tradeperson=False, is_business=False, is_distributor=False, is_deliverer=False)
    serializer_class = UserSerializer
    filterparam = 'is_user'


class BaseAuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @staticmethod
    def login_user(request, serializer_class):
        serializer = serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            refresh = RefreshToken.for_user(user)
            usertypeserilizer_class = UserSerializer
            if user.is_business:
                usertypeserilizer_class = BusinessSerializer
            elif user.is_distributor:
                usertypeserilizer_class = DistributorSerializer
            elif user.is_deliverer:
                usertypeserilizer_class = DelivererSerializer
            elif user.is_tradeperson:
                usertypeserilizer_class = TradePersonSerializer
            else:
                usertypeserilizer_class = UserSerializer
            
            return Response({
                'success': True,
                'message': 'Login successful',
                'user': usertypeserilizer_class(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    def login(self, request):
        return self.login_user(request, UserLoginSerializer)

    def logout(self, request):
        logout(request)
        return Response({'success': True, 'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


class LoginViewSet(BaseAuthViewSet):
    pass


class TradepersonViewSet(BaseUserViewSet, BaseAuthViewSet):
    queryset = User.objects.filter(is_tradeperson=True)
    filterparam = 'is_tradeperson'
    serializer_class = TradePersonSerializer


class BusinessViewSet(BaseUserViewSet, BaseAuthViewSet):
    queryset = User.objects.filter(is_business=True)
    filterparam = 'is_business'
    serializer_class = BusinessSerializer


class DistributorViewSet(BaseUserViewSet, BaseAuthViewSet):
    queryset = User.objects.filter(is_distributor=True)
    filterparam = 'is_distributor'
    serializer_class = DistributorSerializer


class DelivererViewSet(BaseUserViewSet, BaseAuthViewSet):
    queryset = User.objects.filter(is_deliverer=True)
    filterparam = 'is_deliverer'
    serializer_class = DelivererSerializer


class VerifyEmailView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'success': False, 'message': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'success': True, 'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordRequestView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            new_password = request.data.get('new_password')
            confirm_password = request.data.get('confirm_password')
            if new_password != confirm_password:
                return Response({'success': False, 'message': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
            user.password = Util.hash_password(new_password)
            user.save()
            return Response({'success': True, 'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)


class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        # Customize response data
        data = {'success': True,'message': 'Professions retrieved successfully', 'data': serializer.data}
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # Customize response data
        data = {'success': True, 'message': 'Profession retrieved successfully', 'data': serializer.data}
        return Response(data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            # Customize success response
            return Response({'success': True, 'message': 'Profession created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            # Customize error response
            return Response({'success': False, 'message': 'Failed to create profession', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            # Customize success response
            return Response({'success': True, 'message': 'Profession updated successfully', 'data': serializer.data})
        else:
            # Customize error response
            return Response({'success': False, 'message': 'Failed to update profession', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        # Customize success response
        return Response({'success': True, 'message': 'Profession deleted successfully'})