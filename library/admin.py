from django.contrib import admin
from .models import Book, Loan, User, Notification
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

# Register your models here.

class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_bibliotecario', 'user_type', 'academic_year', 'faculty')
    list_filter = ('is_staff', 'is_active', 'is_bibliotecario', 'user_type', 'faculty')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'user_type', 'academic_year', 'faculty')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_bibliotecario', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'is_bibliotecario', 'user_type', 'academic_year', 'faculty')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Book)
admin.site.register(Loan)
admin.site.register(Notification)
