from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from .api.serializers import *
from .models import *
from django.db.models import Q

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from .api.serializers import *
from .models import *
from django.db.models import Q

# Create your views here.
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer  # ← ВАЖНО: используем RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(user).data,
                "message": "Регистрация выполнена успешно"
            }
            , status = status.HTTP_201_CREATED
        )

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({
            'user': UserSerializer(user).data,
            'message': "Выполнен вход"
        })

# Остальные ваши классы остаются без изменений...
# Выход
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Выход выполнен"})

# Текущий пользователь
class CurrentUserView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class PinListCreateView(generics.ListCreateAPIView):
    serializer_class = PinSerializer
    ordering = '-created_at'

    def get_queryset(self):
        return Pin.objects.filter(is_private=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PinDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PinSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Pin.objects.filter(
                models.Q(is_private=False) | models.Q(user=user)
            )
        return Pin.objects.filter(is_private=False)

class BoardListCreateView(generics.ListCreateAPIView):
    serializer_class = BoardSerializer
    ordering = 'title'

    def get_queryset(self):
        return Board.objects.all()

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BoardSerializer
    def get_queryset(self):
        return Board.objects.all()