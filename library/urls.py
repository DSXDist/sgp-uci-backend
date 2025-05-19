# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import BookViewSet, UserViewSet, LoanViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'users', UserViewSet)

users_router = routers.NestedDefaultRouter(router, r'users', lookup='user')
users_router.register(r'loans', LoanViewSet, basename='user-loans')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(users_router.urls)),
    path('api-auth/', include('rest_framework.urls')),  # Para login en browsable API
]
