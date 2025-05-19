from django.contrib.auth.models import AbstractUser
from django.db import models

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
