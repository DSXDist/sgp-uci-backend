from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model, authenticate
from .models import User, Book, Loan, Notification
from .serializers import UserSerializer, BookSerializer, LoanSerializer, NotificationSerializer

class IsBibliotecario(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_bibliotecario

class IsLibrarianOrReadOnly(BasePermission):
    """
    Permite acceso total a bibliotecarios.
    Para otros usuarios, solo lectura.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_bibliotecario:
            return True
        return request.method in SAFE_METHODS

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsBibliotecario()]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsBibliotecario]

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def get_permissions(self):
        if self.request.user.is_authenticated and self.request.user.is_bibliotecario:
            return [IsBibliotecario()]
        # Permitir a usuarios normales crear y ver sus propios préstamos
        if self.action in ['list', 'retrieve', 'create']:
            return [IsAuthenticated()]
        return [IsBibliotecario()]

    def get_queryset(self):
        user_id = self.kwargs.get('user_pk')
        if self.request.user.is_bibliotecario:
            return Loan.objects.all()
        # Usuarios normales solo ven sus préstamos
        return Loan.objects.filter(user=self.request.user)

# Notificaciones: cualquier usuario autenticado puede ver, crear y modificar las suyas
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Solo notificaciones del usuario autenticado
        return Notification.objects.filter(user=self.request.user)

# Vista para crear usuario y devolver token
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

class UserRegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para modificar usuario
class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# Vista para eliminar usuario
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'is_bibliotecario': user.is_bibliotecario,  # o 'is_librarian' si prefieres
        })

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class UserLoansView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        # Solo bibliotecario o el propio usuario puede ver sus préstamos
        if not (request.user.is_bibliotecario or request.user.id == user_id):
            return Response({'detail': 'No autorizado.'}, status=403)
        loans = Loan.objects.filter(user__id=user_id)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)

class UserNotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        # Solo bibliotecario o el propio usuario puede ver sus notificaciones
        if not (request.user.is_bibliotecario or request.user.id == user_id):
            return Response({'detail': 'No autorizado.'}, status=403)
        notifications = Notification.objects.filter(user__id=user_id)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
