# ⚡ Quick Start: Gmail Email Setup

## 🚀 5-Minute Setup

### 1️⃣ Enable 2-Factor Authentication
- Go to: https://myaccount.google.com/security
- Enable **2-Step Verification**

### 2️⃣ Generate App Password
- Go to: https://myaccount.google.com/apppasswords
- Select: **Mail** → **Other** → Name it "Django"
- Click **Generate**
- Copy the 16-character password (remove spaces)

### 3️⃣ Create .env File
```bash
cd backend
cp .env.example .env
```

### 4️⃣ Edit .env File
```env
USE_REAL_EMAIL=true
EMAIL_HOST_USER=yourname@gmail.com
EMAIL_HOST_PASSWORD=abcdefghijklmnop
DEFAULT_FROM_EMAIL=yourname@gmail.com
FRONTEND_URL=http://localhost:4200
```

### 5️⃣ Test It!
```bash
# Start Django
cd backend
python manage.py runserver

# In another terminal, request a password reset
# Or use: python backend/test_password_reset.py
```

## 📋 Example Values

**Your .env should look like:**
```env
USE_REAL_EMAIL=true
EMAIL_HOST_USER=john.doe@gmail.com
EMAIL_HOST_PASSWORD=abcdefghijklmnop
DEFAULT_FROM_EMAIL=john.doe@gmail.com
FRONTEND_URL=http://localhost:4200
```

## 🔄 Development Mode (No Real Emails)

**In .env:**
```env
USE_REAL_EMAIL=false
```

This will print emails to console instead of sending them.

## ✅ That's It!

Password reset emails will now be sent via Gmail! 🎉

**For detailed troubleshooting**, see: `GMAIL_SETUP_GUIDE.md`
