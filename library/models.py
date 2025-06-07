from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('El nombre de usuario es obligatorio')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_bibliotecario', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')
        return self.create_user(username, email, password, **extra_fields)
    
class User(AbstractUser):
    TYPE_CHOICES = [
        ('STUDENT', 'Estudiante'),
        ('TEACHER', 'Profesor'),
        ('WORKER', 'Trabajador'),
    ]
    
    is_bibliotecario = models.BooleanField(default=False)
    user_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='STUDENT')
    academic_year = models.CharField(max_length=20, blank=True, default='N/A')
    faculty = models.PositiveIntegerField(default=1)
    

class Book(models.Model):
    image_url = models.URLField(max_length=200, blank=True, default='')
    title = models.CharField(max_length=200, default='')
    author = models.CharField(max_length=100, default='')
    editorial = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    published_date = models.DateField()
    available_copies = models.PositiveIntegerField(default=1)
    categories = models.CharField(max_length=300, default='')
    
    def __str__(self):
        return self.title
    
class Loan(models.Model):
    
    STATUS_CHOICES = [
        ('AWAITING', 'Esperando aprobacion'),
        ('ONDATE', 'Prestado y en tiempo'),
        ('AWAITING', 'Prestado y fuera de tiempo'),
    ]
    
    user = models.ForeignKey(User, related_name='loans', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='AWAITING')
    
    def __str__(self):
        return self.book.title + "-" + self.user.username

class Notification(models.Model):
    TYPE_CHOICES = [
        ('MULTA', 'Multa'),
        ('VENCIMIENTO', 'Vencimiento'),
        ('DISPONIBILIDAD', 'Disponibilidad'),
        ('SISTEMA', 'Sistema'),
    ]

    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

