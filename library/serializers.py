# serializers.py
from rest_framework import serializers
from .models import User, Book, Loan

class LoanSerializer(serializers.ModelSerializer):
    book_title = serializers.ReadOnlyField(source='book.title')

    class Meta:
        model = Loan
        fields = ['id', 'book', 'book_title', 'loan_date', 'return_date', 'returned']

class UserSerializer(serializers.ModelSerializer):
    loans = LoanSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_bibliotecario', 'loans']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
