from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Comment, Follower
# Register your models here.

admin.site.register(User, UserAdmin)
#admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follower)

