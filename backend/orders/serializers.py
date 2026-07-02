from rest_framework import serializers
from .models import Order, OrderItem, OrderStatusHistory


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
            'payment_id', 'razorpay_order_id', 'created_at', 'items'
        ]
        read_only_fields = ['total_amount', 'status', 'created_at']


# ---------------------------------------------------------------------------
# Admin serializers
# ---------------------------------------------------------------------------

class OrderStatusHistorySerializer(serializers.ModelSerializer):
    changed_by = serializers.SerializerMethodField()

    class Meta:
        model = OrderStatusHistory
        fields = ['id', 'old_status', 'new_status', 'note', 'changed_by', 'changed_at']

    def get_changed_by(self, obj):
        if obj.changed_by:
            return obj.changed_by.email
        return None


class AdminOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)
    customer_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer_email', 'full_name', 'phone',
            'address_line', 'city', 'state', 'pincode',
            'total_amount', 'status', 'payment_method', 'payment_id',
            'razorpay_order_id', 'created_at', 'updated_at',
            'items', 'status_history',
        ]


class OrderUpdateSerializer(serializers.ModelSerializer):
    note = serializers.CharField(write_only=True, required=False, allow_blank=True, default='')

    class Meta:
        model = Order
        fields = ['status', 'note']

    def validate_status(self, value):
        valid = [choice[0] for choice in Order.STATUS_CHOICES]
        if value not in valid:
            raise serializers.ValidationError(f"Invalid status. Choose from: {', '.join(valid)}")
        return value


class AdminLogsSerializer(serializers.ModelSerializer):
    """Serializer for order history logs with related order and user info"""
    order_id = serializers.IntegerField(source='order.id', read_only=True)
    customer_email = serializers.EmailField(source='order.user.email', read_only=True)
    customer_name = serializers.SerializerMethodField()
    changed_by_email = serializers.EmailField(source='changed_by.email', read_only=True, allow_null=True)
    total_amount = serializers.DecimalField(source='order.total_amount', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderStatusHistory
        fields = [
            'id', 'order_id', 'customer_email', 'customer_name', 'total_amount',
            'old_status', 'new_status', 'note', 'changed_by_email', 'changed_at'
        ]

    def get_customer_name(self, obj):
        return obj.order.full_name
