from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductVariant


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    
    class Meta:
        model = Category
        fields = ['id', 'route', 'name', 'text', 'icon', 'image', 'content']


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for ProductImage model"""
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image_path', 'display_order']


class ProductVariantSerializer(serializers.ModelSerializer):
    """Serializer for ProductVariant model"""
    
    class Meta:
        model = ProductVariant
        fields = ['id', 'weight', 'original_price', 'discounted_price']


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for product listings"""
    categories = serializers.StringRelatedField(many=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'short', 'categories', 'images', 'variants']


class ProductDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single product view"""
    categories = CategorySerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'short', 'categories',
            'about', 'footer', 'benefits', 'ingredients',
            'nutritional_value', 'images', 'variants'
        ]


class CategoryWithProductsSerializer(serializers.ModelSerializer):
    """Serializer for category with its products"""
    products = ProductListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'route', 'name', 'text', 'icon', 'image', 'content', 'products']
