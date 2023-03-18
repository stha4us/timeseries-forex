from django.http import HttpResponse, JsonResponse
# Create your views here.
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from .models import User, UserProfile, BlackListedToken
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
from datetime import datetime, timedelta

# class UserRegistrationView(CreateAPIView):
#     serializer_class = UserRegistrationSerializer
#     permission_classes = (AllowAny,)
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         status_code = status.HTTP_201_CREATED
#         response = {
#             'success': 'True',
#             'status code': status_code,
#             'message': 'User registered  successfully',
#         }
#
#         return Response(response, status=status_code)


class UserLoginView(APIView):

    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    # queryset = Post.objects.all()
    queryset = ''

    def post(self, request):
        # useremail = User.objects.all(user=request.email)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return JsonResponse(response, status=status_code, safe=False)

# class UserLogoutView(APIView):
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = JSONWebTokenAuthentication
#
#     def post(self, request):
#         # return self.logout(request)
#         django_logout(request)
#         return JsonResponse(status = 204)

class IsTokenValid(BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        is_allowed_user = True
        token = request.auth.decode("utf-8")
        try:
            is_blackListed = BlackListedToken.objects.get(user=user_id, token=token)
            if is_blackListed:
                is_allowed_user = False
        except BlackListedToken.DoesNotExist:
            is_allowed_user = True
        return is_allowed_user


class UserProfileView(APIView):

    permission_classes = (IsAuthenticated, IsTokenValid)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'first_name': user_profile.first_name,
                    'last_name': user_profile.last_name,
                    'phone_number': user_profile.phone_number,
                    'age': user_profile.age,
                    'gender': user_profile.gender,
                    }]
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
                }
        return JsonResponse(response, status=status_code)


class UserMeView(APIView):
    permission_classes = (IsAuthenticated, IsTokenValid)
    authentication_class = JSONWebTokenAuthentication
    def get(self, request):
        current_user = request.user
        pk = current_user.id
        try:
            user_profile = User.objects.get(pk=pk)
            email=user_profile.email
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User info fetched successfully',
                'data': {
                    'user': user_profile.email,
                }
            }

        except Exception as e:
            email = 'Anonymous User'
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'Sorry user detail not available',
                'error': str(e),
                'data':{
                    'user':email,
                }
            }
        return JsonResponse(response, status=status_code, safe=False)


class SignoutView(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    def post(self, request):
        user = request.user.id
        contents = request.headers
        new_token = contents['Authorization']
        token = new_token.replace('Bearer ','')
        project = BlackListedToken.objects.create(
            token = token,
            user_id = user
        )
        return JsonResponse('Signed out!', status=status.HTTP_200_OK, safe=False)



class ClearBlackList(APIView):
    permission_classes = (IsAuthenticated, IsTokenValid)
    authentication_class = JSONWebTokenAuthentication
    def post(self, request, **kwargs):
        useless = BlackListedToken.objects.filter(timestamp__lt=datetime.now()+timedelta(days=-8))
        useless.delete()
        return JsonResponse('Expired blacktoken cleared', status=status.HTTP_200_OK, safe=False)

# USE THE discard_token view with celery to clear the unnecessary database entires daily
class RemoveBlackList():
    def discard_tokens(self, **kwargs):
        useless = BlackListedToken.objects.filter(timestamp__lt=datetime.now()+timedelta(days=-8))
        useless.delete()

