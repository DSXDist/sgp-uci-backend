# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import BookViewSet, UserViewSet, LoanViewSet
from .views import UserRegisterView, UserUpdateView, UserDeleteView
from .views import CustomAuthToken, NotificationViewSet
from .views import UserLoansView, UserNotificationsView  # <-- Importa las vistas

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'users', UserViewSet)
router.register(r'notifications', NotificationViewSet)  # <-- Agrega esta línea
router.register(r'loans', LoanViewSet)  # <-- Agrega esta línea para endpoint global de préstamos

users_router = routers.NestedDefaultRouter(router, r'users', lookup='user')
users_router.register(r'loans', LoanViewSet, basename='user-loans')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(users_router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('api/register/', UserRegisterView.as_view(), name='user-register'),
    path('api/users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('api/users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('api/users/<int:user_id>/loans/', UserLoansView.as_view(), name='user-loans-list'),  # <-- Nueva línea
    path('api/users/<int:user_id>/notifications/', UserNotificationsView.as_view(), name='user-notifications-list'),  # <-- Nueva línea
]
