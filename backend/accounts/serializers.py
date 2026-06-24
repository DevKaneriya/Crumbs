from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_email(self, value):
        email = value.lower().strip()
        if User.objects.filter(Q(username__iexact=email) | Q(email__iexact=email)).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return email

    def create(self, validated_data):
        email = validated_data['email']
        first_name = validated_data['first_name'].strip()
        last_name = validated_data['last_name'].strip()
        password = validated_data['password']
        return User.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        identifier = attrs.get('email', '').strip()
        password = attrs.get('password')

        if not identifier or not password:
            raise serializers.ValidationError('Email and password are required.')

        user = User.objects.filter(
            Q(username__iexact=identifier) | Q(email__iexact=identifier)
        ).first()

        if user is None:
            raise AuthenticationFailed('Invalid credentials.')

        authenticated_user = authenticate(
            request=self.context.get('request'),
            username=user.username,
            password=password,
        )

        if authenticated_user is None:
            raise AuthenticationFailed('Invalid credentials.')

        refresh = RefreshToken.for_user(authenticated_user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': authenticated_user.id,
                'first_name': authenticated_user.first_name,
                'last_name': authenticated_user.last_name,
                'name': (authenticated_user.get_full_name() or authenticated_user.get_username()),
                'email': authenticated_user.email,
                'username': authenticated_user.get_username(),
            },
        }


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    pass


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return value.lower().strip()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        try:
            # Decode the UID - handle potential padding issues
            uid_str = attrs['uid']
            
            # Add padding if necessary
            missing_padding = len(uid_str) % 4
            if missing_padding:
                uid_str += '=' * (4 - missing_padding)
            
            uid = urlsafe_base64_decode(uid_str).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError) as e:
            raise ValidationError({'uid': ['Invalid user ID.']})
        except User.DoesNotExist:
            raise ValidationError({'uid': ['Invalid user ID.']})

        # Check the token
        if not default_token_generator.check_token(user, attrs['token']):
            raise ValidationError({'token': ['Invalid or expired token.']})

        attrs['user'] = user
        return attrs

    def save(self):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user

