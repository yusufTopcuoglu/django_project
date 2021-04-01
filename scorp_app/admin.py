from django.contrib import admin

from .models import User, Follow, Post

admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Post)
