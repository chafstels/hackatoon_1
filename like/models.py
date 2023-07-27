from django.contrib.auth import get_user_model
from django.db import models
from books.models import Book

User = get_user_model()
# Create your models here.
class Like(models.Model):
    book = models.ForeignKey(Book, related_name='likes', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)

class Favorite(models.Model):
    owner = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='favorites', on_delete=models.CASCADE)
