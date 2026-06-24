# 📧 Gmail SMTP Setup Guide for Production Email

## 🎯 Overview

This guide will help you configure Gmail to send real password reset emails from your Django application.

## 📋 Prerequisites

- A Gmail account
- 2-Factor Authentication enabled on your Gmail account

---

## 🔐 Step-by-Step Setup

### Step 1: Enable 2-Factor Authentication

1. Go to your Google Account: **https://myaccount.google.com/**
2. Click on **Security** in the left sidebar
3. Under "How you sign in to Google", find **2-Step Verification**
4. If not enabled, click on it and follow the setup wizard
5. You'll need your phone to receive verification codes

### Step 2: Generate Gmail App Password

1. After enabling 2FA, go to: **https://myaccount.google.com/apppasswords**
   
   Or navigate manually:
   - Go to https://myaccount.google.com/security
   - Click **2-Step Verification**
   - Scroll down to **App passwords** and click it

2. You may need to sign in again

3. **Select app**: Choose **Mail**

4. **Select device**: Choose **Other (Custom name)**

5. Enter a name like: **"Django Crumbs App"**

6. Click **Generate**

7. **IMPORTANT**: You'll see a 16-character password like: `abcd efgh ijkl mnop`
   - Copy this password immediately
   - Remove the spaces: `abcdefghijklmnop`
   - You won't be able to see it again!

### Step 3: Create Environment File

1. Navigate to your backend directory:
   ```bash
   cd backend
   ```

2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` file with your actual values:
   ```bash
   # Windows
   notepad .env
   
   # Mac/Linux
   nano .env
   # or
   vim .env
   ```

4. Update the values:
   ```env
   USE_REAL_EMAIL=true
   EMAIL_HOST_USER=yourname@gmail.com
   EMAIL_HOST_PASSWORD=abcdefghijklmnop
   DEFAULT_FROM_EMAIL=yourname@gmail.com
   FRONTEND_URL=http://localhost:4200
   ```

### Step 4: Install python-dotenv

To read environment variables from `.env` file:

```bash
cd backend
pip install python-dotenv
```

### Step 5: Update Django to Load .env File

Add this to the top of `backend/main/settings.py` (after imports):

```python
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR.parent / '.env')
```

### Step 6: Test Email Sending

1. Start your Django server:
   ```bash
   cd backend
   python manage.py runserver
   ```

2. Request a password reset from the frontend or use the test script:
   ```bash
   cd backend
   python test_password_reset.py
   ```

3. Check your actual email inbox for the reset email!

---

## 🔄 Switching Between Development and Production

### Development Mode (Console Email)
```env
USE_REAL_EMAIL=false
```
Emails will print to the Django console - good for testing without sending real emails.

### Production Mode (Real Gmail)
```env
USE_REAL_EMAIL=true
EMAIL_HOST_USER=yourname@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```
Emails will be sent via Gmail SMTP.

---

## 🛡️ Security Best Practices

### 1. Never Commit .env to Git

Add to `.gitignore`:
```
.env
*.env
.env.local
```

### 2. Use Different Accounts for Dev/Production

- **Development**: Use a test Gmail account
- **Production**: Use a dedicated business email

### 3. Rotate App Passwords Regularly

- Generate new app passwords periodically
- Revoke old ones from: https://myaccount.google.com/apppasswords

### 4. Monitor Email Usage

- Check your Gmail "Sent" folder regularly
- Set up alerts for unusual activity

---

## 🚀 Production Deployment

For production servers (Heroku, AWS, DigitalOcean, etc.):

### Set Environment Variables on Your Server

```bash
# Heroku
heroku config:set USE_REAL_EMAIL=true
heroku config:set EMAIL_HOST_USER=yourname@gmail.com
heroku config:set EMAIL_HOST_PASSWORD=abcdefghijklmnop
heroku config:set FRONTEND_URL=https://yourapp.com

# AWS / Linux Server
export USE_REAL_EMAIL=true
export EMAIL_HOST_USER=yourname@gmail.com
export EMAIL_HOST_PASSWORD=abcdefghijklmnop
export FRONTEND_URL=https://yourapp.com
```

---

## 🐛 Troubleshooting

### Error: "Username and Password not accepted"

**Cause**: Wrong credentials or app password not generated

**Solution**:
- Make sure 2FA is enabled
- Generate a NEW app password
- Remove spaces from the app password
- Use the app password, NOT your regular Gmail password

### Error: "SMTPAuthenticationError"

**Cause**: Gmail blocking sign-in attempt

**Solution**:
- Check that "Less secure app access" is OFF (it should be)
- Make sure you're using an App Password, not regular password
- Try generating a new app password

### Error: "Connection refused" or "Connection timeout"

**Cause**: Firewall or network blocking SMTP port 587

**Solution**:
- Check firewall settings
- Ensure port 587 is open
- Try from a different network

### Emails Not Arriving

**Check**:
1. Gmail "Sent" folder - was it sent?
2. Recipient's spam folder
3. Check Django logs for errors
4. Verify EMAIL_HOST_USER is correct

---

## 📊 Gmail Sending Limits

**Free Gmail Account**:
- 500 emails per day
- 100-150 emails per hour

If you exceed these limits, Gmail will temporarily block sending.

**Solution**: Use a dedicated email service for high volume:
- SendGrid
- Mailgun
- Amazon SES
- Postmark

---

## 🔀 Alternative: Using Other Email Providers

### Using Outlook/Hotmail
```env
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=yourname@outlook.com
EMAIL_HOST_PASSWORD=your-password
```

### Using SendGrid
```env
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

---

## ✅ Quick Test Checklist

- [ ] 2FA enabled on Gmail
- [ ] App password generated
- [ ] `.env` file created with correct values
- [ ] `python-dotenv` installed
- [ ] Django loads `.env` file
- [ ] `USE_REAL_EMAIL=true` in `.env`
- [ ] Test email sent successfully
- [ ] Email received in inbox

---

## 📞 Need Help?

If you're still having issues:

1. Check Django console for error messages
2. Verify your Gmail settings at https://myaccount.google.com/security
3. Test with the provided test script: `python backend/test_password_reset.py`
4. Check if email appears in your Gmail "Sent" folder

---

## 🎉 Success!

Once configured, your application will send professional password reset emails automatically! 📧✨
