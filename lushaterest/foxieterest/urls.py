from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from . import views

urlpatterns = [
    # Токены
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # Аутентификация
    path('api/auth/register/', views.RegisterView.as_view(),
         name='register'),
    path('api/auth/login/', views.LoginView.as_view(),
         name='login'),
    path('api/auth/logout/', views.LogoutView.as_view(),
         name='logout'),
    path('api/auth/profile/', views.CurrentUserView.as_view(),
         name='current-user'),

    # Посты
    path('api/pins/', views.PinListCreateView.as_view(),
         name='pins_list'),
    path('api/pins/<int:pk>', views.PinDetailView.as_view(),
         name='pins_detail'),

    # Доски
    path('api/boards/', views.BoardListCreateView.as_view(),
         name='boards_list'),
    path('api/boards/<int:pk>', views.BoardDetailView.as_view(),
         name='boards_detail'),

]