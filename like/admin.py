from django.contrib import admin
from .models import Favorite, Like
# Register your models here.

admin.site.register(Favorite)
admin.site.register(Like)