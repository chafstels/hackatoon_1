from django.contrib.auth import get_user_model
from django.db import models
from books.models import Book


User = get_user_model()

# Create your models here.
class Rating(models.Model):
    RATING_CHOICES = (
        (1, 'Too bad'),
        (2, 'Bad'),
        (3, 'Normal'),
        (4, 'Good'),
        (5, 'Excellent'),
    )

    book = models.ForeignKey(Book, related_name='ratings', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['owner', 'book']