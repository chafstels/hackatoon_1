from rest_framework import serializers

from category.models import Category
from comment.serializers import CommentSerializer
from like.serializers import LikeSerializer
from .models import Book, Author, Genre
from django.db.models import Avg


class BookListSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Book
        fields = ('id', 'title', 'price', 'owner_username', 'image', 'category_name', 'stock')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rating'] = instance.ratings.aggregate(
            Avg('rating')
        )
        representation['rating_count'] = instance.ratings.count()
        return representation


class BookDetailSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Book
        fields = '__all__'

    @staticmethod
    def is_liked(book, user):
        return user.likes.filter(book=book).exists()

    @staticmethod
    def is_favorite(book, user):
        return user.favorites.filter(book=book).exists()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = LikeSerializer(instance.likes.all(), many=True).data
        representation['quantity of likes'] = 0
        for _ in representation['likes']:
            representation['quantity of likes'] += 1
        representation['comment_count'] = instance.comments.count()
        representation['comments'] = CommentSerializer(
            instance.comments.all(), many=True
        ).data
        representation['rating'] = instance.ratings.aggregate(Avg('rating'))
        representation['rating_count'] = instance.ratings.count()
        user = self.context['request'].user
        if user.is_authenticated:
            representation['is_liked'] = self.is_liked(instance, user)
            representation['is_favorite'] = self.is_favorite(instance, user)

        return representation


class BookCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(required=True, queryset=Category.objects.all())
    author_id = serializers.PrimaryKeyRelatedField(required=True, queryset=Author.objects.all())
    genre_id = serializers.PrimaryKeyRelatedField(required=True, queryset=Genre.objects.all())
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.ReadOnlyField(source='owner.id')


    class Meta:
        model = Book
        fields = '__all__'


