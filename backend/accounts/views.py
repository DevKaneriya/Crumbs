from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
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

        response = Response(
            {
                'message': 'Login successful.',
                'user': data['user'],
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
            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # Ensure uid is a string
            uid_str = uid.decode() if isinstance(uid, bytes) else uid
            
            # Build reset URL - DON'T use urlencode for email links
            # The browser will handle the URL parameters correctly
            reset_url = f"{settings.FRONTEND_URL}/account/reset-password?uid={uid_str}&token={token}"
            
            # Print to console for easy copying during development
            print(f"\n{'='*60}")
            print(f"PASSWORD RESET LINK FOR: {user.email}")
            print(f"{'='*60}")
            print(f"{reset_url}")
            print(f"{'='*60}\n")
            
            # Send email - use plain text without special formatting
            subject = 'Password Reset Request'
            message = f"""Hello {user.first_name or user.username},

You requested a password reset for your Crumbs account.

Click the link below to reset your password:
{reset_url}

This link will expire in 1 hour.

If you didn't request this, please ignore this email.

Best regards,
The Crumbs Team"""
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                # Log the error but don't reveal it to the user
                print(f"Error sending password reset email: {e}")

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
            user = serializer.save()
            
            return Response(
                {
                    'message': 'Password has been reset successfully. You can now login with your new password.'
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {'error': 'An error occurred while resetting your password.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
