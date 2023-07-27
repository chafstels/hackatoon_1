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
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        post = self.context.get('post')
        post = Book.objects.get(pk=post)
        validated_data['post'] = post
        owner = self.context.get('owner')
        validated_data['owner'] = owner
        return super().create(validated_data)