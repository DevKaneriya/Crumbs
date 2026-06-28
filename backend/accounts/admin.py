from django.contrib import admin
from .models import CartItem, WishlistItem, Address

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'variant', 'quantity', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__name', 'variant')

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__name')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'city', 'state', 'is_default', 'created_at')
    list_filter = ('is_default', 'created_at', 'city', 'state')
    search_fields = ('user__username', 'first_name', 'last_name', 'address', 'city', 'pin_code')
