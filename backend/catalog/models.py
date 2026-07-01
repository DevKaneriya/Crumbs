from django.db import models

class Category(models.Model):
    """
    Category model for organizing products
    """
    # route acts as a URL slug (e.g. 'sugar-free')
    route = models.SlugField(max_length=100, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    text = models.CharField(max_length=100, blank=True)
    icon = models.CharField(max_length=255, blank=True)  # Path to asset
    image = models.CharField(max_length=255, blank=True)  # Path to asset
    content = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product model representing individual products
    """
    name = models.CharField(max_length=255)
    # short acts as product url slug (e.g. 'digestive-mukhwas')
    short = models.SlugField(max_length=255, unique=True, db_index=True)
    categories = models.ManyToManyField(Category, related_name='products')
    
    # Description fields (previously 'discription')
    about = models.TextField(blank=True, null=True)
    footer = models.TextField(blank=True, null=True)
    
    # Store list arrays directly as JSON
    benefits = models.JSONField(default=list, blank=True)  # ['Aids digestion', 'Freshens breath']
    ingredients = models.JSONField(default=list, blank=True)  # ['Fennel Seeds', 'Coriander Seeds']
    
    # Store key-value objects directly as JSON
    nutritional_value = models.JSONField(default=dict, blank=True)  # {'Fats': '7.62g', 'Energy': '334 Kcal'}

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """
    Product images with display ordering
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_path = models.CharField(max_length=255)  # e.g., 'assets/products/sugar-free/digestive-mukhwas.webp'
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self):
        return f"{self.product.name} - Image {self.display_order}"


class ProductVariant(models.Model):
    """
    Product variants with pricing information
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    weight = models.CharField(max_length=50)  # e.g. '75gm', '150gm'
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)  # Stock availability toggle

    class Meta:
        ordering = ['original_price']
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"

    def __str__(self):
        return f"{self.product.name} - {self.weight}"
