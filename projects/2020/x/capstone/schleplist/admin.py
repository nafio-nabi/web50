from django.contrib import admin

from .models import User, NewPost, Bookmark

# Register your models here.
admin.site.register(User)
admin.site.register(NewPost)
admin.site.register(Bookmark)