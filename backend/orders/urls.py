from django.urls import path
from .views import (
    # Customer
    CheckoutView,
    MyOrdersView,
    MyOrderDetailView,
    # Razorpay payment
    CreateRazorpayOrderView,
    VerifyRazorpayPaymentView,
    RazorpayWebhookView,
    # Admin / store owner
    AdminOrderListView,
    AdminOrderDetailView,
    AdminOrderUpdateView,
    AdminOrderStatsView,
    AdminCustomerInsightsView,
    AdminLogsView,
)

urlpatterns = [
    # ------------------------------------------------------------------
    # Customer endpoints
    # ------------------------------------------------------------------
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('my-orders/', MyOrdersView.as_view(), name='my_orders'),
    path('my-orders/<int:pk>/', MyOrderDetailView.as_view(), name='my_order_detail'),

    # ------------------------------------------------------------------
    # Razorpay payment endpoints
    # ------------------------------------------------------------------
    path('razorpay/create-order/',   CreateRazorpayOrderView.as_view(),   name='razorpay_create_order'),
    path('razorpay/verify-payment/', VerifyRazorpayPaymentView.as_view(), name='razorpay_verify_payment'),
    path('razorpay/webhook/',        RazorpayWebhookView.as_view(),        name='razorpay_webhook'),

    # ------------------------------------------------------------------
    # Store-owner / admin endpoints  (is_staff required)
    # ------------------------------------------------------------------
    path('admin/', AdminOrderListView.as_view(), name='admin_order_list'),
    path('admin/stats/', AdminOrderStatsView.as_view(), name='admin_order_stats'),
    path('admin/customers/', AdminCustomerInsightsView.as_view(), name='admin_customers'),
    path('admin/logs/', AdminLogsView.as_view(), name='admin_logs'),
    path('admin/<int:pk>/', AdminOrderDetailView.as_view(), name='admin_order_detail'),
    path('admin/<int:pk>/update/', AdminOrderUpdateView.as_view(), name='admin_order_update'),
]
