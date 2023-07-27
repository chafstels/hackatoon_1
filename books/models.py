from django.db import models
from django.contrib.auth import get_user_model
from category.models import Category
# Create your models here.

User = get_user_model()

class Author(models.Model):
    name_author = models.CharField(max_length=100)

    def __str__(self):
        return self.name_author

class Genre(models.Model):
    name_genre = models.CharField(max_length=100)

    def __str__(self):
        return self.name_genre

class Book(models.Model):
    STATUS_CHOICES = (('in_stock', 'В наличии'),('out_of_stock', 'Нет в наличии'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    image = models.ImageField(upload_to='images')
    price = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.CharField(max_length=50, choices=STATUS_CHOICES)
    amount = models.PositiveSmallIntegerField()
    author_id = models.ForeignKey(Author, on_delete=models.PROTECT, related_name='books')
    genre_id = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Книги'
        verbose_name_plural = 'Книги'
