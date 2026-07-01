from django.contrib import admin
from .models import Order, OrderItem, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'variant_weight', 'quantity', 'price_at_purchase', 'get_subtotal')
    fields = ('product_name', 'variant_weight', 'quantity', 'price_at_purchase', 'get_subtotal')

    def get_subtotal(self, obj):
        return f"Rs. {obj.get_subtotal()}"
    get_subtotal.short_description = 'Subtotal'


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ('old_status', 'new_status', 'note', 'changed_by', 'changed_at')
    fields = ('changed_at', 'old_status', 'new_status', 'note', 'changed_by')
    ordering = ('-changed_at',)
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'total_amount', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('id', 'user__email', 'full_name', 'phone', 'pincode')
    readonly_fields = (
        'user', 'full_name', 'phone', 'address_line', 'city', 'state', 'pincode',
        'total_amount', 'payment_method', 'payment_id', 'created_at', 'updated_at',
    )
    list_editable = ('status',)
    ordering = ('-created_at',)
    inlines = [OrderItemInline, OrderStatusHistoryInline]

    fieldsets = (
        ('Order Info', {
            'fields': ('user', 'status', 'total_amount', 'payment_method', 'payment_id', 'created_at', 'updated_at')
        }),
        ('Shipping Address', {
            'fields': ('full_name', 'phone', 'address_line', 'city', 'state', 'pincode')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product_name', 'variant_weight', 'quantity', 'price_at_purchase')
    search_fields = ('product_name', 'order__id', 'order__user__email')
    readonly_fields = ('order', 'product', 'product_name', 'variant_weight', 'quantity', 'price_at_purchase')


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'old_status', 'new_status', 'changed_by', 'changed_at')
    list_filter = ('new_status', 'changed_at')
    search_fields = ('order__id', 'order__user__email')
    readonly_fields = ('order', 'old_status', 'new_status', 'note', 'changed_by', 'changed_at')
    ordering = ('-changed_at',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
