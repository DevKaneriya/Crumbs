from django.urls import path

from .views import (
    CsrfView,
    LoginView,
    LogoutView,
    MeView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    RegisterView,
    SessionView,
    TokenRefreshView,
    CartSyncView,
    CartAddView,
    CartRemoveView,
    CartClearView,
    WishlistSyncView,
    WishlistToggleView,
    WishlistClearView,
)

urlpatterns = [
    path('csrf/', CsrfView.as_view(), name='csrf'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
    path('session/', SessionView.as_view(), name='session'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('cart/sync/', CartSyncView.as_view(), name='cart_sync'),
    path('cart/add/', CartAddView.as_view(), name='cart_add'),
    path('cart/remove/', CartRemoveView.as_view(), name='cart_remove'),
    path('cart/clear/', CartClearView.as_view(), name='cart_clear'),
    path('wishlist/sync/', WishlistSyncView.as_view(), name='wishlist_sync'),
    path('wishlist/toggle/', WishlistToggleView.as_view(), name='wishlist_toggle'),
    path('wishlist/clear/', WishlistClearView.as_view(), name='wishlist_clear'),
]
