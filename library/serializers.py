# serializers.py
from rest_framework import serializers
from .models import User, Book, Loan, Notification

class LoanSerializer(serializers.ModelSerializer):
    book_title = serializers.ReadOnlyField(source='book.title')
    returned = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = ['id', 'book', 'book_title', 'loan_date', 'return_date', 'status', 'returned']  # Cambia 'returned' por 'status'

    def get_returned(self, obj):
        # Considera como "devuelto" si return_date no es None
        return obj.return_date is not None

class UserSerializer(serializers.ModelSerializer):
    loans = LoanSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True, required=True)
    user_type = serializers.CharField(required=False)
    academic_year = serializers.CharField(required=False)
    faculty = serializers.IntegerField(required=False)
    is_bibliotecario = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'is_bibliotecario',
            'user_type', 'academic_year', 'faculty', 'loans'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
