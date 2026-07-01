from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer
from catalog.models import Product, ProductVariant
from accounts.models import CartItem
from decimal import Decimal

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        
        # 1. Fetch user's cart from DB (which was synced prior to checkout)
        cart_items = CartItem.objects.filter(user=user)
        
        if not cart_items.exists():
            return Response({'error': 'Your cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 2. Extract shipping info from request
        full_name = data.get('full_name')
        phone = data.get('phone')
        address_line = data.get('address_line')
        city = data.get('city')
        state = data.get('state')
        pincode = data.get('pincode')
        payment_method = data.get('payment_method', 'COD')

        if not all([full_name, phone, address_line, city, state, pincode]):
            return Response({'error': 'Please provide all shipping details.'}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Calculate total and verify prices directly from DB
        total_amount = Decimal('0.00')
        order_items_data = []

        for item in cart_items:
            try:
                product = Product.objects.get(id=item.product_id)
                variant = ProductVariant.objects.get(product=product, weight=item.variant)
                price = variant.discounted_price
                total_amount += (price * item.quantity)
                
                order_items_data.append({
                    'product': product,
                    'product_name': product.name,
                    'variant_weight': item.variant,
                    'quantity': item.quantity,
                    'price_at_purchase': price
                })
            except (Product.DoesNotExist, ProductVariant.DoesNotExist):
                return Response({'error': f'Product or variant not found for item {item.product_id}'}, status=status.HTTP_400_BAD_REQUEST)

        # 4. Create Order
        order = Order.objects.create(
            user=user,
            full_name=full_name,
            phone=phone,
            address_line=address_line,
            city=city,
            state=state,
            pincode=pincode,
            total_amount=total_amount,
            payment_method=payment_method,
            status='Pending'
        )

        # 5. Create Order Items
        for item_data in order_items_data:
            OrderItem.objects.create(
                order=order,
                product=item_data['product'],
                product_name=item_data['product_name'],
                variant_weight=item_data['variant_weight'],
                quantity=item_data['quantity'],
                price_at_purchase=item_data['price_at_purchase']
            )

        # 6. Clear Cart
        cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MyOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
