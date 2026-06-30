from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .serializers import (
    CategorySerializer,
    CategoryWithProductsSerializer,
    ProductListSerializer,
    ProductDetailSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for categories
    
    list: Get all categories
    retrieve: Get a single category by route (slug)
    products: Get all products in a category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'route'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'text']

    @method_decorator(cache_page(60 * 15))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'products':
            return CategoryWithProductsSerializer
        return CategorySerializer

    @action(detail=True, methods=['get'])
    def products(self, request, route=None):
        """Get all products in a specific category"""
        category = self.get_object()
        serializer = CategoryWithProductsSerializer(category)
        return Response(serializer.data)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for products
    
    list: Get all products (with optional filtering)
    retrieve: Get a single product by short (slug)
    """
    queryset = Product.objects.prefetch_related('categories', 'images', 'variants').all()
    lookup_field = 'short'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categories__route']
    search_fields = ['name', 'about', 'ingredients']
    ordering_fields = ['name', 'id']
    ordering = ['name']

    @method_decorator(cache_page(60 * 15))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer
