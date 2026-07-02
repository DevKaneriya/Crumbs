from django.db.models import Q, Count, Sum, Max
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

import razorpay
import hmac
import hashlib
import json
import logging

from django.conf import settings as django_settings

from .models import Order, OrderItem, OrderStatusHistory
from .serializers import OrderSerializer, AdminOrderSerializer, OrderUpdateSerializer, AdminLogsSerializer
from catalog.models import Product, ProductVariant
from accounts.models import CartItem
from decimal import Decimal

logger = logging.getLogger(__name__)


# ===========================================================================
# Customer views
# ===========================================================================

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
                
                # Check if variant is in stock
                if not variant.in_stock:
                    return Response(
                        {'error': f'{product.name} ({item.variant}) is currently out of stock. Please remove it from your cart and try again.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
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
                return Response(
                    {'error': f'Product or variant not found for item {item.product_id}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

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
        orders = Order.objects.filter(user=request.user).prefetch_related('items')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyOrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ===========================================================================
# Store-owner / admin views  (require is_staff=True)
# ===========================================================================

class AdminOrderListView(APIView):
    """
    GET /api/orders/admin/
    Query params:
      - status   : filter by order status  (e.g. ?status=Pending)
      - payment  : filter by payment method (e.g. ?payment=COD)
      - search   : match order id, customer email or full name
      - date_from / date_to : YYYY-MM-DD range on created_at
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        queryset = (
            Order.objects
            .select_related('user')
            .prefetch_related('items', 'status_history')
            .order_by('-created_at')
        )

        status_filter = request.query_params.get('status')
        payment_filter = request.query_params.get('payment')
        search = request.query_params.get('search')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if payment_filter:
            queryset = queryset.filter(payment_method=payment_filter)
        if search:
            queryset = queryset.filter(
                Q(id__icontains=search) |
                Q(user__email__icontains=search) |
                Q(full_name__icontains=search) |
                Q(phone__icontains=search)
            )
        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)

        serializer = AdminOrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminOrderDetailView(APIView):
    """
    GET /api/orders/admin/<pk>/
    Full detail for a single order including items and full status history.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        order = get_object_or_404(
            Order.objects.select_related('user').prefetch_related('items', 'status_history__changed_by'),
            pk=pk
        )
        serializer = AdminOrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminOrderUpdateView(APIView):
    """
    PATCH /api/orders/admin/<pk>/update/
    Body: { "status": "Shipped", "note": "optional internal note" }
    Records a history entry whenever the status actually changes.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderUpdateSerializer(order, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        old_status = order.status
        note = serializer.validated_data.pop('note', '')
        serializer.save()

        # Log history only when status actually changed
        new_status = order.status
        if old_status != new_status:
            OrderStatusHistory.objects.create(
                order=order,
                old_status=old_status,
                new_status=new_status,
                note=note,
                changed_by=request.user,
            )

        return Response(AdminOrderSerializer(order).data, status=status.HTTP_200_OK)


class AdminOrderStatsView(APIView):
    """
    GET /api/orders/admin/stats/
    Returns aggregate counts and revenue for the dashboard summary cards.
    Also includes top products, revenue trend, and customer counts.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        from django.contrib.auth import get_user_model
        from django.utils import timezone
        import datetime

        User = get_user_model()

        # --- Order status counts & revenue ---
        stats = Order.objects.aggregate(
            total_orders=Count('id'),
            total_revenue=Sum('total_amount'),
            pending=Count('id', filter=Q(status='Pending')),
            paid=Count('id', filter=Q(status='Paid')),
            shipped=Count('id', filter=Q(status='Shipped')),
            delivered=Count('id', filter=Q(status='Delivered')),
            cancelled=Count('id', filter=Q(status='Cancelled')),
        )
        if stats['total_revenue'] is None:
            stats['total_revenue'] = 0

        # --- Orders in last 30 days ---
        thirty_days_ago = timezone.now() - datetime.timedelta(days=30)
        recent_stats = Order.objects.filter(created_at__gte=thirty_days_ago).aggregate(
            recent_orders=Count('id'),
            recent_revenue=Sum('total_amount'),
        )
        stats['recent_orders'] = recent_stats['recent_orders'] or 0
        stats['recent_revenue'] = recent_stats['recent_revenue'] or 0

        # --- Total unique customers ---
        stats['total_customers'] = User.objects.filter(is_staff=False).count()
        stats['customers_with_orders'] = Order.objects.values('user').distinct().count()

        # --- Top 5 selling products (by units sold) ---
        top_products = (
            OrderItem.objects
            .values('product_name')
            .annotate(units_sold=Sum('quantity'), revenue=Sum('price_at_purchase'))
            .order_by('-units_sold')[:5]
        )
        stats['top_products'] = list(top_products)

        # --- Daily orders for last 7 days ---
        seven_days_ago = timezone.now() - datetime.timedelta(days=7)
        daily = (
            Order.objects
            .filter(created_at__gte=seven_days_ago)
            .extra(select={'day': "date(created_at)"})
            .values('day')
            .annotate(count=Count('id'), revenue=Sum('total_amount'))
            .order_by('day')
        )
        stats['daily_trend'] = list(daily)

        return Response(stats, status=status.HTTP_200_OK)


class AdminCustomerInsightsView(APIView):
    """
    GET /api/orders/admin/customers/
    Returns customer list with order history and spending data.
    Supports ?search= and ?ordering=total_spent|-total_spent|orders|-orders
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        search = request.query_params.get('search', '').strip()
        ordering = request.query_params.get('ordering', '-total_spent')

        # Aggregate order data per user
        customers = (
            Order.objects
            .values('user__id', 'user__email', 'user__first_name', 'user__last_name')
            .annotate(
                total_orders=Count('id'),
                total_spent=Sum('total_amount'),
                last_order=Max('created_at'),
                delivered_orders=Count('id', filter=Q(status='Delivered')),
                cancelled_orders=Count('id', filter=Q(status='Cancelled')),
            )
        )

        if search:
            customers = customers.filter(
                Q(user__email__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search)
            )

        # Ordering
        valid_orderings = {
            'total_spent': 'total_spent',
            '-total_spent': '-total_spent',
            'orders': 'total_orders',
            '-orders': '-total_orders',
            'last_order': 'last_order',
            '-last_order': '-last_order',
        }
        db_ordering = valid_orderings.get(ordering, '-total_spent')
        customers = customers.order_by(db_ordering)

        result = []
        for c in customers:
            result.append({
                'user_id': c['user__id'],
                'email': c['user__email'],
                'first_name': c['user__first_name'] or '',
                'last_name': c['user__last_name'] or '',
                'total_orders': c['total_orders'],
                'total_spent': float(c['total_spent'] or 0),
                'last_order': c['last_order'],
                'delivered_orders': c['delivered_orders'],
                'cancelled_orders': c['cancelled_orders'],
            })

        return Response(result, status=status.HTTP_200_OK)


class AdminLogsView(APIView):
    """
    GET /api/orders/admin/logs/
    Returns all order status change logs with filters.
    Query params:
      - status_from: filter by old_status (e.g. ?status_from=Pending)
      - status_to: filter by new_status (e.g. ?status_to=Shipped)
      - search: search by order ID, customer email, or customer name
      - date_from / date_to: YYYY-MM-DD range on changed_at
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        queryset = (
            OrderStatusHistory.objects
            .select_related('order__user', 'changed_by')
            .order_by('-changed_at')
        )

        status_from = request.query_params.get('status_from')
        status_to = request.query_params.get('status_to')
        search = request.query_params.get('search')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        if status_from:
            queryset = queryset.filter(old_status=status_from)
        if status_to:
            queryset = queryset.filter(new_status=status_to)
        if search:
            queryset = queryset.filter(
                Q(order__id__icontains=search) |
                Q(order__user__email__icontains=search) |
                Q(order__full_name__icontains=search)
            )
        if date_from:
            queryset = queryset.filter(changed_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(changed_at__date__lte=date_to)

        serializer = AdminLogsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ===========================================================================
# Razorpay payment views
# ===========================================================================

def _razorpay_client():
    """Return an authenticated Razorpay client using settings credentials."""
    return razorpay.Client(
        auth=(django_settings.RAZORPAY_KEY_ID, django_settings.RAZORPAY_KEY_SECRET)
    )


def _build_order_items_data(cart_items):
    """
    Validate cart against DB prices and return (total_amount, order_items_data).
    Raises ValueError with a user-facing message on any issue.
    """
    total_amount = Decimal('0.00')
    order_items_data = []

    for item in cart_items:
        try:
            product = Product.objects.get(id=item.product_id)
            variant = ProductVariant.objects.get(product=product, weight=item.variant)
        except (Product.DoesNotExist, ProductVariant.DoesNotExist):
            raise ValueError(f'Product or variant not found for item {item.product_id}')

        if not variant.in_stock:
            raise ValueError(
                f'{product.name} ({item.variant}) is currently out of stock. '
                'Please remove it from your cart and try again.'
            )

        price = variant.discounted_price
        total_amount += price * item.quantity
        order_items_data.append({
            'product': product,
            'product_name': product.name,
            'variant_weight': item.variant,
            'quantity': item.quantity,
            'price_at_purchase': price,
        })

    return total_amount, order_items_data


class CreateRazorpayOrderView(APIView):
    """
    POST /api/orders/razorpay/create-order/

    Step 1 of the Razorpay flow. Validates the cart, creates a Razorpay order,
    persists a Django Order (status=Pending) and returns the data needed to
    open the Razorpay checkout modal on the frontend.

    Request body:
        full_name, phone, address_line, city, state, pincode, payment_method
    Response:
        { razorpay_order_id, amount, currency, key_id, order_db_id }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        # 1. Validate cart
        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            return Response({'error': 'Your cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Validate shipping details
        full_name    = data.get('full_name', '').strip()
        phone        = data.get('phone', '').strip()
        address_line = data.get('address_line', '').strip()
        city         = data.get('city', '').strip()
        state        = data.get('state', '').strip()
        pincode      = data.get('pincode', '').strip()
        payment_method = data.get('payment_method', 'Card')

        if not all([full_name, phone, address_line, city, state, pincode]):
            return Response(
                {'error': 'Please provide all shipping details.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Calculate total from DB (server-side; never trust client prices)
        try:
            total_amount, order_items_data = _build_order_items_data(cart_items)
        except ValueError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        # 4. Create Razorpay order (amount in paise — multiply by 100)
        try:
            client = _razorpay_client()
            rz_order = client.order.create({
                'amount': int(total_amount * 100),  # paise
                'currency': 'INR',
                'receipt': f'crumbs_user_{user.id}',
                'payment_capture': 1,               # auto-capture on payment
            })
        except Exception as exc:
            logger.error('Razorpay order creation failed: %s', exc, exc_info=True)
            return Response(
                {'error': 'Payment gateway error. Please try again.'},
                status=status.HTTP_502_BAD_GATEWAY
            )

        # 5. Persist a Django Order (Pending — confirmed only after payment verify)
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
            status='Pending',
            razorpay_order_id=rz_order['id'],
        )

        for item_data in order_items_data:
            OrderItem.objects.create(
                order=order,
                product=item_data['product'],
                product_name=item_data['product_name'],
                variant_weight=item_data['variant_weight'],
                quantity=item_data['quantity'],
                price_at_purchase=item_data['price_at_purchase'],
            )

        return Response({
            'razorpay_order_id': rz_order['id'],
            'amount':            rz_order['amount'],   # paise
            'currency':          rz_order['currency'],
            'key_id':            django_settings.RAZORPAY_KEY_ID,
            'order_db_id':       order.id,
        }, status=status.HTTP_201_CREATED)


class VerifyRazorpayPaymentView(APIView):
    """
    POST /api/orders/razorpay/verify-payment/

    Step 2 of the Razorpay flow. Called by the frontend after the Razorpay
    modal reports a successful payment. Verifies the HMAC-SHA256 signature,
    marks the order as Paid, clears the cart, and returns the completed order.

    Request body:
        razorpay_order_id, razorpay_payment_id, razorpay_signature, order_db_id
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        razorpay_order_id   = data.get('razorpay_order_id', '')
        razorpay_payment_id = data.get('razorpay_payment_id', '')
        razorpay_signature  = data.get('razorpay_signature', '')
        order_db_id         = data.get('order_db_id')

        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature, order_db_id]):
            return Response({'error': 'Missing payment verification fields.'}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Fetch the Django order — must belong to the logged-in user
        order = get_object_or_404(Order, pk=order_db_id, user=request.user)

        # Guard: already verified (idempotent)
        if order.status == 'Paid':
            from .serializers import OrderSerializer as OS
            return Response(OS(order).data, status=status.HTTP_200_OK)

        # 2. Verify HMAC-SHA256 signature
        try:
            client = _razorpay_client()
            client.utility.verify_payment_signature({
                'razorpay_order_id':   razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature':  razorpay_signature,
            })
        except razorpay.errors.SignatureVerificationError:
            logger.warning(
                'Razorpay signature mismatch for order %s (rzp order %s)',
                order_db_id, razorpay_order_id
            )
            # Mark the pending order as Cancelled so it doesn't sit open forever
            order.status = 'Cancelled'
            order.save(update_fields=['status', 'updated_at'])
            return Response(
                {'error': 'Payment verification failed. Your order has been cancelled.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Mark order as Paid and record the Razorpay payment ID
        old_status   = order.status
        order.status     = 'Paid'
        order.payment_id = razorpay_payment_id
        order.save(update_fields=['status', 'payment_id', 'updated_at'])

        OrderStatusHistory.objects.create(
            order=order,
            old_status=old_status,
            new_status='Paid',
            note=f'Razorpay payment captured: {razorpay_payment_id}',
        )

        # 4. Clear the user's cart
        CartItem.objects.filter(user=request.user).delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class RazorpayWebhookView(APIView):
    """
    POST /api/orders/razorpay/webhook/

    Receives Razorpay webhook events and updates order status accordingly.
    Acts as a reliable backstop in case the frontend verify call never reaches
    the backend (network drop, browser close, etc.).

    Supported events:
        payment.captured  → order status Paid
        payment.failed    → order status Cancelled

    Security: validates X-Razorpay-Signature header using RAZORPAY_WEBHOOK_SECRET.
    """
    authentication_classes = []   # webhooks are not user-authenticated
    permission_classes = []

    def post(self, request):
        webhook_secret = django_settings.RAZORPAY_WEBHOOK_SECRET

        # 1. Verify webhook signature if secret is configured
        if webhook_secret:
            received_sig = request.headers.get('X-Razorpay-Signature', '')
            body_bytes   = request.body  # raw bytes — must read before DRF parses

            expected_sig = hmac.new(
                webhook_secret.encode('utf-8'),
                body_bytes,
                hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(expected_sig, received_sig):
                logger.warning('Razorpay webhook: invalid signature')
                return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Parse event
        try:
            payload = json.loads(request.body)
        except (json.JSONDecodeError, Exception):
            return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

        event = payload.get('event', '')

        if event == 'payment.captured':
            self._handle_payment_captured(payload)

        elif event == 'payment.failed':
            self._handle_payment_failed(payload)

        # Always return 200 so Razorpay doesn't keep retrying
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)

    # ── helpers ──────────────────────────────────────────────────────────────

    def _handle_payment_captured(self, payload):
        try:
            payment_entity   = payload['payload']['payment']['entity']
            razorpay_order_id  = payment_entity.get('order_id', '')
            razorpay_payment_id = payment_entity.get('id', '')

            order = Order.objects.filter(razorpay_order_id=razorpay_order_id).first()
            if not order:
                logger.warning('Webhook payment.captured: no order for rzp order %s', razorpay_order_id)
                return

            if order.status == 'Paid':
                return  # Already processed — idempotent

            old_status       = order.status
            order.status     = 'Paid'
            order.payment_id = razorpay_payment_id
            order.save(update_fields=['status', 'payment_id', 'updated_at'])

            OrderStatusHistory.objects.create(
                order=order,
                old_status=old_status,
                new_status='Paid',
                note=f'[Webhook] Razorpay payment captured: {razorpay_payment_id}',
            )

            # Clear cart as a safety net (normally cleared during verify step)
            CartItem.objects.filter(user=order.user).delete()

            logger.info('Webhook: order #%s marked Paid via payment.captured', order.id)

        except (KeyError, Exception) as exc:
            logger.error('Webhook payment.captured handler error: %s', exc)

    def _handle_payment_failed(self, payload):
        try:
            payment_entity    = payload['payload']['payment']['entity']
            razorpay_order_id = payment_entity.get('order_id', '')

            order = Order.objects.filter(razorpay_order_id=razorpay_order_id).first()
            if not order or order.status in ('Paid', 'Shipped', 'Delivered', 'Cancelled'):
                return

            old_status   = order.status
            order.status = 'Cancelled'
            order.save(update_fields=['status', 'updated_at'])

            OrderStatusHistory.objects.create(
                order=order,
                old_status=old_status,
                new_status='Cancelled',
                note='[Webhook] Razorpay payment failed',
            )

            logger.info('Webhook: order #%s cancelled via payment.failed', order.id)

        except (KeyError, Exception) as exc:
            logger.error('Webhook payment.failed handler error: %s', exc)
