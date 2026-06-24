#!/usr/bin/env python
"""
Test script for password reset functionality.
Run with: python backend/test_password_reset.py
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from urllib.parse import urlencode

User = get_user_model()

def test_password_reset():
    print("\n=== Testing Password Reset Functionality ===\n")
    
    # Get or create a test user
    email = "test@example.com"
    try:
        user = User.objects.get(username=email)
        print(f"✓ Found existing test user: {user.username}")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name="Test",
            last_name="User",
            password="oldpassword123"
        )
        print(f"✓ Created test user: {user.username}")
    
    print(f"  User ID: {user.pk}")
    print(f"  Email: {user.email}")
    
    # Generate token
    token = default_token_generator.make_token(user)
    print(f"\n✓ Generated token: {token}")
    
    # Encode UID
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    uid_str = uid.decode() if isinstance(uid, bytes) else uid
    print(f"✓ Encoded UID: {uid_str}")
    
    # Test decoding
    try:
        decoded_uid = urlsafe_base64_decode(uid_str).decode()
        print(f"✓ Decoded UID: {decoded_uid}")
        assert str(user.pk) == decoded_uid, "UID mismatch!"
    except Exception as e:
        print(f"✗ Error decoding UID: {e}")
        return False
    
    # Test token validation
    is_valid = default_token_generator.check_token(user, token)
    print(f"\n✓ Token validation: {is_valid}")
    
    if is_valid:
        # Build properly encoded URL
        params = {'uid': uid_str, 'token': token}
        query_string = urlencode(params)
        reset_url = f"http://localhost:4200/account/reset-password?{query_string}"
        
        print("\n=== Test Data for Frontend ===")
        print(f"Reset URL (copy this entire line):")
        print(f"{reset_url}")
        print(f"\nOR use these values separately:")
        print(f"  uid: {uid_str}")
        print(f"  token: {token}")
        print(f"  new_password: newpassword123")
        
        print("\n=== cURL Test Command ===")
        print(f"""curl -X POST http://localhost:8000/api/accounts/password-reset-confirm/ \\
  -H "Content-Type: application/json" \\
  -d '{{"uid": "{uid_str}", "token": "{token}", "new_password": "newpassword123"}}'""")
    else:
        print("\n✗ Token validation failed!")
        return False
    
    print("\n=== All Tests Passed ===\n")
    return True

if __name__ == "__main__":
    test_password_reset()
