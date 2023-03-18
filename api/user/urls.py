from django.urls import path, include
from .views import UserLoginView, UserProfileView, UserMeView \
    # UserLogoutView, UserRegistrationView
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token
# from django.contrib.auth import views as auth_views

# from django.conf import settings
from user.views import SignoutView, ClearBlackList

# from rest_framework.routers import SimpleRouter
# router =SimpleRouter()
# router.register('login', UserLogoutView, base_name="login")
# urlpatterns = router.urls

urlpatterns = [
    # path(r'signup/', UserRegistrationView.as_view(), name='usersignup'),
    # path(r'auth/login/', UserLoginView.as_view(), name='userlogin'),
    path(r'auth/login/', obtain_jwt_token, name='userlogin'),
    path(r'auth/refresh-token/', refresh_jwt_token, name='refreshtoken'),
    path('auth/signout/', SignoutView.as_view(), name='signout'),
    path(r'auth/profile/', UserProfileView.as_view(), name='userprofile'),
    path(r'auth/me/',UserMeView.as_view(), name='useremail'),
    path(r'auth/clear-token/',ClearBlackList.as_view(), name='clear-token'),
    # path(r'auth/logout/', UserLogoutView.as_view(), name='userlogout'),
    # path('auth/logout/', auth_views.LogoutView.as_view(), {
    #     'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

    ]