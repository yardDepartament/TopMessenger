from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatViewSet, MessageViewSet, UserProfileViewSet, register_user, auth_user, get_user_data, logout_user

router = DefaultRouter()
router.register(r'chats', ChatViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'user_profiles', UserProfileViewSet)
# router.register(r'register_user', register_user)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_user, name='register_user'),
    path('auth/', auth_user, name='auth_user'),
    path('get_user_data/', get_user_data, name='get_user_data'),
    path('logout/', logout_user, name='logout_user'),
]
