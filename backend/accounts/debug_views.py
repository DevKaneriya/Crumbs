"""
Debug views to troubleshoot cookie issues in production.
Remove this file after debugging.
"""
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(['GET'])
@permission_classes([AllowAny])
def debug_cookies(request):
    """Debug endpoint to see cookie configuration and what's being received."""
    return JsonResponse({
        'received_cookies': dict(request.COOKIES),
        'settings': {
            'DEBUG': settings.DEBUG,
            'CORS_ALLOW_CREDENTIALS': settings.CORS_ALLOW_CREDENTIALS,
            'CORS_ALLOWED_ORIGINS': settings.CORS_ALLOWED_ORIGINS,
            'CSRF_TRUSTED_ORIGINS': settings.CSRF_TRUSTED_ORIGINS,
            'AUTH_COOKIE_SECURE': settings.AUTH_COOKIE_SECURE,
            'AUTH_COOKIE_SAMESITE': settings.AUTH_COOKIE_SAMESITE,
            'AUTH_COOKIE_HTTP_ONLY': settings.AUTH_COOKIE_HTTP_ONLY,
        },
        'headers': {
            'Origin': request.headers.get('Origin'),
            'Referer': request.headers.get('Referer'),
        }
    })
