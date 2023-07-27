from rest_framework import serializers
from .models import Comment
from books.models import Book


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = '__all__'

class CommentActionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    book = serializers.ReadOnlyField(source='book.id')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        book = self.context.get('book')
        book = Book.objects.get(pk=book)
        validated_data['book'] = book
        owner = self.context.get('owner')
        validated_data['owner'] = owner
        return super().create(validated_data)