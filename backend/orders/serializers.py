from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'variant_weight', 'quantity', 'price_at_purchase', 'subtotal']

    def get_subtotal(self, obj):
        return obj.get_subtotal()


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'full_name', 'phone', 'address_line', 'city',
            'state', 'pincode', 'total_amount', 'status', 'payment_method',
            'payment_id', 'created_at', 'items'
        ]
        read_only_fields = ['total_amount', 'status', 'created_at']
