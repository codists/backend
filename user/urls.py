from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('signup/', UserViewSet.as_view({'post': 'signup'}), name='user_signup'),
    path('signin/', UserViewSet.as_view({'post': 'signin'}), name='user_signin'),
    path('me/', UserViewSet.as_view({'get': 'me'}), name='user_me'),
    path('', include(router.urls)),
]
