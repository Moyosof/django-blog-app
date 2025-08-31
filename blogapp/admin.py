from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Blog, CustomUser
# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'bio', 
                    'profile_picture', 'youtube', 'facebook', 'instagram', 'twitter')

admin.site.register(CustomUser, CustomUserAdmin) # registering both model and user admin class


class BlogAdmin(admin.ModelAdmin):
    list_display = ( "title", "author", "created_at", "is_draft", "category")

admin.site.register(Blog, BlogAdmin)