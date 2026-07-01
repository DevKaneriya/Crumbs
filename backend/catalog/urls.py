from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, AdminStockListView, AdminStockToggleView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    # Admin stock management
    path('admin/stock/', AdminStockListView.as_view(), name='admin_stock_list'),
    path('admin/stock/<int:pk>/', AdminStockToggleView.as_view(), name='admin_stock_toggle'),
]
