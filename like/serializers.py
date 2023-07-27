from rest_framework import serializers
from .models import Like, Favorite

class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Like
        fields = '__all__'

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        book = attrs['book']
        if user.likes.filter(book=book).exists():
            raise serializers.ValidationError(
                'you have already liked this book!'
            )
        return attrs

class LikedUserSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Like
        fields = ['owner', 'owner_username']

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('id', 'book')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['book_title'] = instance.book.title
        if instance.book.image:
            preview = instance.book.image
            representation['book_preview'] = preview.url
        else:
            representation['book_preview'] = None
        return representation

class FavoriteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
