from pyexpat import model
from django.contrib import admin

from .models import User, Post

class UserModel(admin.ModelAdmin):
    list_display = ("id", "username")

class PostModel(admin.ModelAdmin):
    list_display = ("id", "post", "user", "timestamp")

# Register your models here.
admin.site.register(User, UserModel)
admin.site.register(Post, PostModel)