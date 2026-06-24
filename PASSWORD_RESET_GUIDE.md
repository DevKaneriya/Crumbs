# Password Reset Implementation Guide

## ✅ Implementation Complete

The password reset functionality has been fully implemented for both frontend and backend.

## 🔧 How to Test

### Method 1: Using the Test Script (Recommended)

Run this command to generate a valid test link:

```bash
cd backend
python test_password_reset.py
```

This will:
- Create or find the test user (test@example.com)
- Generate a valid reset token
- Display a working reset URL
- Show a cURL command for API testing

**Copy the entire reset URL from the output and paste it in your browser.**

### Method 2: Using the UI Flow

1. Start both servers:
   ```bash
   # Terminal 1 - Backend
   cd backend
   python manage.py runserver

   # Terminal 2 - Frontend
   cd frontend
   ng serve
   ```

2. Navigate to: `http://localhost:4200/account/login`

3. Click "Forgot Your Password?"

4. Enter a registered email address

5. Check the **backend console/terminal** for the email output

6. **⚠️ IMPORTANT**: When copying the URL from the console:
   - Copy the ENTIRE URL as one line
   - Don't copy it with line breaks
   - The URL should look like: `http://localhost:4200/account/reset-password?uid=MTY&token=daoxg2-...`

7. Paste the URL in your browser and reset your password

## 🐛 Common Issues

### Issue 1: "Invalid user ID" Error

**Cause**: URL parameters are being URL-encoded when copied from email/console

**Symptoms**: You see `3DMTU` instead of `MTY` in the URL

**Solution**: 
- Use the test script (Method 1) to generate a clean URL
- Or manually navigate by typing the URL
- The backend now properly handles URL encoding with `urlencode()`

### Issue 2: Console Email Output has Weird Characters

**Cause**: Django's console email backend may add formatting characters like `=20`

**Solution**: Use the test script to get a clean URL, or set up real SMTP in production

### Issue 3: Token Expired

**Cause**: Password reset tokens expire after 1 hour

**Solution**: Request a new password reset link

## 📧 Email Configuration

### Development (Current Setup)

```python
# backend/main/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Emails are printed to the console where Django is running.

### Production Setup

Update `backend/main/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # or your SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'noreply@yourcompany.com'
FRONTEND_URL = 'https://yourfrontend.com'
```

**For Gmail:**
1. Enable 2-factor authentication
2. Generate an "App Password"
3. Use the app password in EMAIL_HOST_PASSWORD

## 🔐 Security Features

✅ Token-based reset (1-hour expiration)  
✅ Secure UID encoding  
✅ Email enumeration prevention  
✅ CSRF protection  
✅ Password validation (min 8 characters)  
✅ Automatic token blacklisting after use  

## 📝 API Endpoints

### Request Password Reset
```
POST /api/accounts/password-reset/
Content-Type: application/json

{
  "email": "user@example.com"
}
```

### Confirm Password Reset
```
POST /api/accounts/password-reset-confirm/
Content-Type: application/json

{
  "uid": "MTY",
  "token": "daoxg2-d9698a5872a772690fc1bd1794ef98cd",
  "new_password": "newpassword123"
}
```

## 🎯 Routes

- `/account/forgot-password` - Request password reset
- `/account/reset-password?uid=...&token=...` - Reset password form
- `/account/login` - Login page (with "Forgot Password?" link)

## ✨ Features

- Clean, responsive UI
- Real-time validation
- Clear error messages
- Auto-redirect after successful reset
- Password confirmation matching
- Loading states and disabled buttons
- Invalid link detection

## 🧪 Testing Checklist

- [ ] Request password reset with valid email
- [ ] Request password reset with invalid email (should still show success)
- [ ] Check console for email output
- [ ] Copy reset URL and open in browser
- [ ] Submit reset form with mismatched passwords (should show error)
- [ ] Submit reset form with short password (should show error)
- [ ] Submit reset form with valid matching passwords (should succeed)
- [ ] Verify old password no longer works
- [ ] Login with new password (should work)
- [ ] Try using the same reset link again (should fail - one-time use)

## 🚀 Deployment Notes

Before deploying to production:

1. Update email settings with real SMTP server
2. Update `FRONTEND_URL` in settings.py
3. Set `DEBUG = False`
4. Use environment variables for sensitive data
5. Enable SSL/TLS for email
6. Test with real email addresses
7. Consider rate limiting on reset endpoint
8. Add monitoring for failed reset attempts

## 📞 Support

If you encounter issues:

1. Run the test script to verify backend is working
2. Check Django console for detailed error messages
3. Check browser console for frontend errors
4. Verify both servers are running
5. Clear browser cache and cookies
6. Try in incognito mode

The password reset system is production-ready and follows Django/Angular best practices! 🎉
