# 📧 Set Up Gmail to Send Real Emails - 5 Minutes

## 🎯 Goal
Get Gmail working so you can receive password reset emails in your actual Gmail inbox.

---

## ⚡ Quick Steps (5 minutes)

### Step 1: Get Gmail App Password (3 minutes)

1. **Open your Gmail account settings**:
   - Go to: **https://myaccount.google.com/security**

2. **Enable 2-Factor Authentication** (if not already enabled):
   - Look for "2-Step Verification" section
   - Click on it and follow the setup
   - You'll need your phone to receive codes
   - ⚠️ **This is required** - App Passwords only work with 2FA enabled

3. **Generate App Password**:
   - After 2FA is enabled, go to: **https://myaccount.google.com/apppasswords**
   - Or scroll down on the security page to find "App passwords"
   - Click "App passwords"
   - Sign in again if asked
   
4. **Create the password**:
   - Select app: **Mail**
   - Select device: **Other (Custom name)**
   - Type: **"Django Crumbs"** or any name
   - Click **Generate**

5. **Copy the password**:
   - You'll see a 16-character password like: `abcd efgh ijkl mnop`
   - **IMPORTANT**: Copy it and remove the spaces: `abcdefghijklmnop`
   - Save it somewhere safe (you won't see it again!)

### Step 2: Update .env File (1 minute)

1. **Open** `backend/.env` file in your editor

2. **Update these 3 lines**:
   ```env
   USE_REAL_EMAIL=true
   EMAIL_HOST_USER=your-actual-email@gmail.com
   EMAIL_HOST_PASSWORD=abcdefghijklmnop
   ```
   
   Replace with:
   - `your-actual-email@gmail.com` → Your real Gmail address
   - `abcdefghijklmnop` → The 16-character App Password you copied (no spaces!)

3. **Save the file**

### Step 3: Test It! (1 minute)

**Run the test script:**
```bash
cd backend
python test_gmail_setup.py
```

**Expected output if successful:**
```
✅ SUCCESS! Test email sent successfully!
   Check your inbox: your-email@gmail.com
```

**Check your Gmail inbox** - you should see a test email!

---

## ✅ That's It!

Now when you request a password reset:
1. Go to: `http://localhost:4200/account/login`
2. Click "Forgot Your Password?"
3. Enter your Gmail address
4. **Check your Gmail inbox** - you'll receive the reset email!

---

## 🐛 Troubleshooting

### Issue: "Username and Password not accepted"

**Causes:**
- Using your regular Gmail password instead of App Password
- App Password has spaces (remove them!)
- 2-Factor Authentication not enabled
- Wrong email address

**Solution:**
1. Make sure 2FA is enabled: https://myaccount.google.com/security
2. Generate a NEW App Password: https://myaccount.google.com/apppasswords
3. Copy it WITHOUT spaces
4. Update `.env` file again
5. Restart Django server

### Issue: "Connection refused" or "Connection timeout"

**Causes:**
- Firewall blocking port 587
- Antivirus blocking connection
- No internet connection

**Solution:**
- Check your internet connection
- Temporarily disable firewall/antivirus to test
- Try on a different network

### Issue: No email received

**Check:**
1. Gmail Spam folder
2. Promotions tab in Gmail
3. Check Django console output - look for error messages
4. Make sure Django server restarted after editing .env

---

## 📝 Example .env File

Your `backend/.env` should look like this:

```env
DEBUG=true
ALLOWED_HOSTS=localhost,127.0.0.1,testserver

# IMPORTANT: Set these 3 values!
USE_REAL_EMAIL=true
EMAIL_HOST_USER=john.doe@gmail.com
EMAIL_HOST_PASSWORD=abcdefghijklmnop

DEFAULT_FROM_EMAIL=noreply@crumbs.com
FRONTEND_URL=http://localhost:4200
```

---

## 🔄 Switch Back to Console Mode (Development)

If you want to go back to printing emails to console:

**Just change one line in `.env`:**
```env
USE_REAL_EMAIL=false
```

Everything else stays the same!

---

## ✨ Quick Reference

| Step | Action | Time |
|------|--------|------|
| 1 | Enable 2FA on Gmail | 2 min |
| 2 | Generate App Password | 1 min |
| 3 | Update .env file | 1 min |
| 4 | Test with script | 1 min |
| **Total** | | **5 min** |

---

## 📞 Need Help?

1. Run `python backend/test_gmail_setup.py` - it will show you exactly what's wrong
2. Check error messages in Django console when requesting password reset
3. Make sure Django server was restarted after editing .env

**You've got this! 🚀**
