from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS, BasePermission
from .models import User, Book, Loan
from .serializers import UserSerializer, BookSerializer, LoanSerializer

class IsBibliotecario(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_bibliotecario

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsBibliotecario]

class LoanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsBibliotecario]

    def get_queryset(self):
        user_id = self.kwargs.get('user_pk')
        if user_id:
            return Loan.objects.filter(user__id=user_id)
        return super().get_queryset()
