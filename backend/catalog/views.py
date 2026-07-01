from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, ProductVariant
from .serializers import (
    CategorySerializer,
    CategoryWithProductsSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    AdminStockVariantSerializer,
    AdminStockToggleSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for categories
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


# ===========================================================================
# Admin stock management views
# ===========================================================================

class AdminStockListView(APIView):
    """
    GET /api/catalog/admin/stock/
    Returns all product variants with their in_stock status.
    Supports ?search= to filter by product name.
    Supports ?in_stock=true|false to filter by stock status.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        queryset = ProductVariant.objects.select_related('product').order_by(
            'product__name', 'original_price'
        )
        search = request.query_params.get('search', '').strip()
        stock_filter = request.query_params.get('in_stock', '')

        if search:
            queryset = queryset.filter(product__name__icontains=search)
        if stock_filter.lower() == 'true':
            queryset = queryset.filter(in_stock=True)
        elif stock_filter.lower() == 'false':
            queryset = queryset.filter(in_stock=False)

        serializer = AdminStockVariantSerializer(queryset, many=True)
        return Response(serializer.data)


class AdminStockToggleView(APIView):
    """
    PATCH /api/catalog/admin/stock/<pk>/
    Body: { "in_stock": true|false }
    Toggles the in_stock flag for a specific variant.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, pk):
        variant = get_object_or_404(ProductVariant, pk=pk)
        serializer = AdminStockToggleSerializer(variant, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        variant.refresh_from_db()  # ensure we return the actual saved value
        return Response(AdminStockVariantSerializer(variant).data, status=status.HTTP_200_OK)
