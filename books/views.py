from django.shortcuts import render

from comment.serializers import CommentActionSerializer, CommentSerializer
from like.models import Like, Favorite
from like.serializers import LikedUserSerializer, FavoriteDetailSerializer
from .models import Book
from .serializers import BookListSerializer, BookDetailSerializer, BookCreateSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .permissions import IsAuthor
from rest_framework.decorators import action
from rating.serializers import RatingSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
class StandartResultPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    pagination_class = StandartResultPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('title', 'category__id')
    filterset_fields = ('title', 'category')

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return BookCreateSerializer
        return BookDetailSerializer


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return permissions.IsAuthenticated(), IsAuthor()
        return (permissions.IsAuthenticatedOrReadOnly(),)


    @action(['GET', 'POST', 'DELETE'], detail=True)
    def ratings(self, request, pk):
        product = self.get_object()
        user = request.user

        if request.method == 'GET':
            rating = product.ratings.all()
            serializer = RatingSerializer(instance=rating, many=True)
            return Response(serializer.data, status=200)

        elif request.method == 'POST':
            if product.ratings.filter(owner=user).exists():
                return Response('Ты уже поставил рейтинг на этот продукт', status=400)
            serializer = RatingSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=user, product=product)
            return Response(serializer.data, status=201)

        else:
            if not product.ratings.filter(owner=user).exists():
                return Response('Ты не можешь удалить, потому что ты не ставил рейтинг этому продукту', status=400)
            rating = product.ratings.get(owner=user)
            rating.delete()
            return Response('Успешно удалено', status=204)

    @action(['GET', 'POST', 'DELETE'], detail=True)
    def like(self, request, pk):
        book = self.get_object()
        user = request.user
        if request.method == 'POST':
            if user.likes.filter(book=book).exists():
                return Response('This post has already liked', status=201)
            Like.objects.create(owner=user, book=book)
            return Response('You have liked this post', status=201)
        elif request.method == 'DELETE':
            likes = user.likes.filter(book=book)
            if likes.exists():
                likes.delete()
                return Response('Like is deleted', status=204)
            return Response('Post is not found', status=404)
        else:
            likes = book.likes.all()
            serializer = LikedUserSerializer(instance=likes, many=True)
            return Response(serializer.data, status=200)

    @action(['GET', 'POST', 'DELETE'], detail=True)
    def comment(self, request, pk):
        book = self.get_object()
        user = request.user
        if request.method == 'POST':
            serializer = CommentActionSerializer(data=request.data, context={'book': book.id, 'owner': user})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == 'DELETE':
            comment_id = self.request.query_params['id']
            comment = book.comments.filter(book=book, pk=comment_id)
            comment.delete()
            return Response('The comment is delete', status=204)
        else:
            comments = book.comments.all()
            serializer = CommentSerializer(instance=comments, many=True)
            return Response(serializer.data, status=200)

    @action(['POST', 'DELETE', 'GET'], detail=True)
    def favorite(self, request, pk):
        book = self.get_object()
        user = request.user
        if request.method == 'POST':
            if user.favorites.filter(book=book).exists():
                return Response('This post already in favorite', status=400)
            Favorite.objects.create(owner=user, book=book)
            return Response('Added to the favorites', status=201)
        elif request.method == 'DELETE':
            favorite = user.favorites.filter(book=book)
            if favorite.exists():
                favorite.delete()
                return Response('You deleted post is Favorites', status=204)
            return Response('Post is not founded', status=404)
        else:
            favorites = user.favorites.all()
            if favorites.exists():
                serializer = FavoriteDetailSerializer(instance=favorites, many=True)
                return Response(serializer.data, status=200)
