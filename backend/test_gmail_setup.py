#!/usr/bin/env python
"""
Gmail SMTP Configuration Test Script
This will help you verify your Gmail setup is working
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_gmail_connection():
    print("\n" + "="*60)
    print("Gmail SMTP Configuration Test")
    print("="*60 + "\n")
    
    # Check configuration
    print("📋 Current Email Configuration:")
    print(f"   USE_REAL_EMAIL: {os.environ.get('USE_REAL_EMAIL', 'False')}")
    print(f"   EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"   EMAIL_HOST_USER: {os.environ.get('EMAIL_HOST_USER', 'Not set')}")
    print(f"   EMAIL_HOST_PASSWORD: {'*' * len(os.environ.get('EMAIL_HOST_PASSWORD', '')) if os.environ.get('EMAIL_HOST_PASSWORD') else 'Not set'}")
    print()
    
    if not os.environ.get('USE_REAL_EMAIL', 'False').lower() == 'true':
        print("⚠️  USE_REAL_EMAIL is set to 'false'")
        print("   Emails will be printed to console, not sent via Gmail.\n")
        print("To test real Gmail sending:")
        print("   1. Edit backend/.env")
        print("   2. Set USE_REAL_EMAIL=true")
        print("   3. Fill in EMAIL_HOST_USER and EMAIL_HOST_PASSWORD")
        print("   4. Run this script again\n")
        return False
    
    # Check if credentials are set
    if not os.environ.get('EMAIL_HOST_USER') or not os.environ.get('EMAIL_HOST_PASSWORD'):
        print("❌ Gmail credentials not configured!")
        print("\n📝 Please follow these steps:\n")
        print("1. Edit backend/.env file")
        print("2. Set EMAIL_HOST_USER to your Gmail address")
        print("3. Set EMAIL_HOST_PASSWORD to your Gmail App Password")
        print("4. Run this script again\n")
        return False
    
    # Test sending email
    recipient = os.environ.get('EMAIL_HOST_USER')
    
    print(f"📧 Attempting to send test email to: {recipient}\n")
    
    try:
        send_mail(
            subject='Crumbs - Gmail Setup Test',
            message='Congratulations! Your Gmail SMTP setup is working correctly. You can now send password reset emails.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        print("✅ SUCCESS! Test email sent successfully!")
        print(f"   Check your inbox: {recipient}")
        print(f"   (Also check spam folder if you don't see it)")
        print()
        return True
        
    except Exception as e:
        print("❌ FAILED to send email!")
        print(f"   Error: {str(e)}\n")
        
        if "Username and Password not accepted" in str(e):
            print("🔧 Common causes:")
            print("   1. Wrong email or password")
            print("   2. Not using App Password (regular password won't work)")
            print("   3. 2-Factor Authentication not enabled")
            print()
            print("✅ Solution:")
            print("   1. Go to: https://myaccount.google.com/security")
            print("   2. Enable 2-Factor Authentication")
            print("   3. Go to: https://myaccount.google.com/apppasswords")
            print("   4. Generate App Password for 'Mail'")
            print("   5. Copy the 16-character password")
            print("   6. Update EMAIL_HOST_PASSWORD in .env")
            print()
        elif "Connection" in str(e):
            print("🔧 Network issue:")
            print("   - Check your internet connection")
            print("   - Firewall might be blocking port 587")
            print()
        
        return False

if __name__ == "__main__":
    success = test_gmail_connection()
    print("="*60 + "\n")
    
    if success:
        print("🎉 Gmail is configured and working!")
        print("   You can now send password reset emails.")
    else:
        print("⚠️  Gmail not configured yet or has issues.")
        print("   Follow the steps above to complete setup.")
    
    print()
