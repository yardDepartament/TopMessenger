from rest_framework import viewsets
from .models import Chat, Message, UserProfile
from .serializers import ChatSerializer, MessageSerializer, UserProfileSerializer
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


@csrf_exempt
@transaction.atomic
def register_user(request):
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Создайте пользователя
        user = User.objects.create_user(username=username, password=password)

        # Создайте профиль пользователя с ключами
        profile = UserProfile(user=user)
        profile.generate_key_pair()

        user.save()
        profile.save()

        # Сохраняем данные в сессии
        request.session['user_id'] = profile.id
        request.session['username'] = profile.user.username
        request.session['public_key'] = profile.public_key
        request.session['private_key'] = profile.private_key

        profile_data = {
            'user_id': profile.id,
            'username': profile.user.username,
            'public_key': profile.public_key,
        }

        print('Пользователь успешно добавлен')
        
        return JsonResponse(profile_data)

    except Exception as e:
        transaction.set_rollback(True)
        return JsonResponse({'message': f'Error in registration user: {e}'})


@csrf_exempt
def auth_user(request):
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        profile = UserProfile.objects.get(user=user)
        
        if user is not None:
            login(request, user)

            # Сохраняем данные в сессии
            request.session['user_id'] = profile.id
            request.session['username'] = profile.user.username
            request.session['public_key'] = profile.public_key
            request.session['private_key'] = profile.private_key

            return JsonResponse({'message': 'Authentication successful'})
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=401)

    except Exception as e:
        print(e)
        return JsonResponse({'message': f'Error in login: {e}'}, status=500)
    
    
@login_required
@csrf_exempt
def get_user_data(request):
    
    print('________________________________________________________________________')
    for key, value in request.session.items():
        print(key, value)
    print('________________________________________________________________________')
    try:
        user_data = {
            'user_id': request.session.get('user_id'),
            'username': request.session.get('username'),
            'first_name': request.session.get('first_name'),
            'last_name': request.session.get('last_name'),
        }

        return JsonResponse(user_data)
    except Exception as e:
        return JsonResponse({'message': f'Error in getting user data: {e}'}, status=500)


def logout_user(request):
    try:
        # Выход пользователя
        logout(request)

        # Опционально: очистка данных сессии
        request.session.flush()

        return JsonResponse({'message': 'Logout successful'})
    except Exception as e:
        return JsonResponse({'message': f'Error in logout: {e}'}, status=500)

# Create your views here.
