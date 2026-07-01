from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductVariant


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    
    class Meta:
        model = Category
        fields = ['id', 'route', 'name', 'text', 'icon', 'image', 'content', 'display_order']


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for ProductImage model"""
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image_path', 'display_order']


class ProductVariantSerializer(serializers.ModelSerializer):
    """Serializer for ProductVariant model — includes in_stock for frontend"""
    
    class Meta:
        model = ProductVariant
        fields = ['id', 'weight', 'original_price', 'discounted_price', 'in_stock']


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


# ---------------------------------------------------------------------------
# Admin stock serializer
# ---------------------------------------------------------------------------

class AdminStockVariantSerializer(serializers.ModelSerializer):
    """Serializer for admin stock management — shows product name alongside variant"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_short = serializers.CharField(source='product.short', read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'product_name', 'product_short', 'weight', 'original_price', 'discounted_price', 'in_stock']


class AdminStockToggleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['in_stock']
