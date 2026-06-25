from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVariant


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'route', 'text']
    search_fields = ['name', 'route']
    prepopulated_fields = {'route': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'short', 'get_categories']
    search_fields = ['name', 'short']
    list_filter = ['categories']
    filter_horizontal = ['categories']
    prepopulated_fields = {'short': ('name',)}
    inlines = [ProductImageInline, ProductVariantInline]

    def get_categories(self, obj):
        return ", ".join([cat.name for cat in obj.categories.all()])
    get_categories.short_description = 'Categories'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_path', 'display_order']
    list_filter = ['product']
    ordering = ['product', 'display_order']


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'weight', 'original_price', 'discounted_price']
    list_filter = ['product']
    search_fields = ['product__name', 'weight']
