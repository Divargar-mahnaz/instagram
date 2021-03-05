from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ['user_name', 'image', 'full_name', 'gender', 'bio', 'website', 'email', 'phone_number', 'following']
    list_display = ['user_name', 'image', 'full_name', 'gender', 'phone_number']
