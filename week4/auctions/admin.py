from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Listing, Comment, Bid
# Register your models here.

admin.site.register(User, UserAdmin)
#admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bid)
