from rest_framework import serializers
from .models import Rating

class RatingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    book = serializers.ReadOnlyField(source='book.title')

    class Meta:
        model = Rating
        fields = '__all__'