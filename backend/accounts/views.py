from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    CookieTokenRefreshSerializer,
    LoginSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
)
from .tasks import (
    send_password_reset_email_task,
    send_registration_success_email_task,
    send_login_success_email_task,
)

User = get_user_model()


def _set_auth_cookies(response, access_token, refresh_token=None):
    response.set_cookie(
        settings.AUTH_COOKIE_ACCESS,
        access_token,
        max_age=settings.AUTH_COOKIE_MAX_AGE_ACCESS,
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=settings.AUTH_COOKIE_SAMESITE,
        path='/',
    )
    if refresh_token is not None:
        response.set_cookie(
            settings.AUTH_COOKIE_REFRESH,
            refresh_token,
            max_age=settings.AUTH_COOKIE_MAX_AGE_REFRESH,
            httponly=settings.AUTH_COOKIE_HTTP_ONLY,
            secure=settings.AUTH_COOKIE_SECURE,
            samesite=settings.AUTH_COOKIE_SAMESITE,
            path='/',
        )


def _clear_auth_cookies(response):
    response.delete_cookie(settings.AUTH_COOKIE_ACCESS, path='/')
    response.delete_cookie(settings.AUTH_COOKIE_REFRESH, path='/')


def _user_payload(user):
    return {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'name': (user.get_full_name() or user.get_username()),
        'email': user.email,
        'username': user.get_username(),
        'is_staff': user.is_staff,
    }


@method_decorator(ensure_csrf_cookie, name='dispatch')
class CsrfView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return JsonResponse({'detail': 'CSRF cookie set.'})


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Send welcome email asynchronously via Celery
        send_registration_success_email_task.delay(user.email, user.first_name or user.username)

        refresh = RefreshToken.for_user(user)
        response = Response(
            {
                'message': 'Registration successful.',
                'user': _user_payload(user),
            },
            status=status.HTTP_201_CREATED,
        )
        _set_auth_cookies(response, str(refresh.access_token), str(refresh))
        return response


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user_payload = data['user']
        # Send login notification email asynchronously via Celery
        send_login_success_email_task.delay(user_payload['email'], user_payload['name'])

        response = Response(
            {
                'message': 'Login successful.',
                'user': user_payload,
            },
            status=status.HTTP_200_OK,
        )
        _set_auth_cookies(response, data['access'], data['refresh'])
        return response


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get(settings.AUTH_COOKIE_REFRESH)
        if not refresh_token:
            return Response(
                {'detail': 'Refresh token not found.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = CookieTokenRefreshSerializer(data={'refresh': refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError:
            return Response(
                {'detail': 'Refresh token is invalid or blacklisted.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        data = serializer.validated_data

        response = Response({'message': 'Token refreshed.'}, status=status.HTTP_200_OK)
        _set_auth_cookies(response, data['access'], data.get('refresh'))
        return response


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get(settings.AUTH_COOKIE_REFRESH)
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                pass

        response = Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
        _clear_auth_cookies(response)
        return response


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'user': _user_payload(request.user)}, status=status.HTTP_200_OK)


class SessionView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            return Response(
                {
                    'authenticated': True,
                    'user': _user_payload(request.user),
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {'authenticated': False, 'user': None},
            status=status.HTTP_200_OK,
        )


class PasswordResetRequestView(APIView):
    """
    Request a password reset. Sends an email with reset link.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.filter(
            Q(username__iexact=email) | Q(email__iexact=email)
        ).first()

        # Always return success to prevent email enumeration
        if user and user.email:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            uid_str = uid.decode() if isinstance(uid, bytes) else uid

            reset_url = f"{settings.FRONTEND_URL}/account/reset-password?uid={uid_str}&token={token}"

            print(f"\n{'='*60}")
            print(f"PASSWORD RESET LINK FOR: {user.email}")
            print(f"{'='*60}")
            print(f"{reset_url}")
            print(f"{'='*60}\n")

            subject = 'Password Reset Request'
            message = f"""Hello {user.first_name or user.username},

You requested a password reset for your Crumbs account.

Click the link below to reset your password:
{reset_url}

This link will expire in 1 hour.

If you didn't request this, please ignore this email.

Best regards,
The Crumbs Team"""

            # Send email asynchronously using Celery
            send_password_reset_email_task.delay(subject, message, user.email)

        return Response(
            {
                'message': 'If an account exists with this email, you will receive a password reset link shortly.'
            },
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):
    """
    Confirm password reset with token and set new password.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer.save()
            return Response(
                {
                    'message': 'Password has been reset successfully. You can now login with your new password.'
                },
                status=status.HTTP_200_OK,
            )
        except Exception:
            return Response(
                {'error': 'An error occurred while resetting your password.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ─── Cart & Wishlist ───────────────────────────────────────────────────────────

from .models import CartItem, WishlistItem
from .serializers import CartItemSerializer, WishlistItemSerializer
from catalog.models import Product


class CartSyncView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return the user's DB cart — used on session restore."""
        cart_items = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Merge local guest cart into DB — used on fresh login only.

        Merge strategy: additive (x + y).
        - x = quantity already in the user's DB cart from a previous session.
        - y = quantity the user added as a guest before logging in.
        - Result = x + y, preserving both the saved account cart and the guest additions.
        """
        local_items = request.data.get('items', [])
        user = request.user

        for item in local_items:
            try:
                product_id = item.get('productId')
                variant = item.get('variant')
                quantity = item.get('quantity', 1)

                product = Product.objects.get(id=product_id)
                cart_item, created = CartItem.objects.get_or_create(
                    user=user, product=product, variant=variant,
                    defaults={'quantity': quantity}
                )
                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()
            except Product.DoesNotExist:
                continue

        cart_items = CartItem.objects.filter(user=user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('productId')
        variant = request.data.get('variant')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user, product=product, variant=variant,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                if cart_item.quantity <= 0:
                    cart_item.delete()
                else:
                    cart_item.save()
            elif quantity <= 0:
                cart_item.delete()

            return Response({'message': 'Cart updated'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


class CartRemoveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('productId')
        variant = request.data.get('variant')
        CartItem.objects.filter(user=request.user, product_id=product_id, variant=variant).delete()
        return Response({'message': 'Item removed'}, status=status.HTTP_200_OK)


class CartClearView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        CartItem.objects.filter(user=request.user).delete()
        return Response({'message': 'Cart cleared'}, status=status.HTTP_200_OK)


class WishlistSyncView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return the user's DB wishlist — used on session restore."""
        wishlist_items = WishlistItem.objects.filter(user=request.user).values_list('product_id', flat=True)
        return Response(list(wishlist_items), status=status.HTTP_200_OK)

    def post(self, request):
        """Merge local guest wishlist into DB — used on fresh login only."""
        local_items = request.data.get('items', [])
        user = request.user

        for product_id in local_items:
            try:
                product = Product.objects.get(id=product_id)
                WishlistItem.objects.get_or_create(user=user, product=product)
            except Product.DoesNotExist:
                continue

        wishlist_items = WishlistItem.objects.filter(user=user).values_list('product_id', flat=True)
        return Response(list(wishlist_items), status=status.HTTP_200_OK)


class WishlistToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('productId')
        try:
            product = Product.objects.get(id=product_id)
            item = WishlistItem.objects.filter(user=request.user, product=product).first()
            if item:
                item.delete()
            else:
                WishlistItem.objects.create(user=request.user, product=product)
            return Response({'message': 'Success'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


class WishlistClearView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        WishlistItem.objects.filter(user=request.user).delete()
        return Response({'message': 'Wishlist cleared'}, status=status.HTTP_200_OK)


# ─── Address ──────────────────────────────────────────────────────────────────

from rest_framework import generics
from .models import Address
from .serializers import AddressSerializer


class AddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user).order_by('-is_default', '-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddressRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
