from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Category
from rest_framework.permissions import AllowAny, IsAdminUser
from .serializers import CategorySerializer
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return (AllowAny(),)
        return (IsAdminUser(),)
