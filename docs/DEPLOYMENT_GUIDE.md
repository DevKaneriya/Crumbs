# Free Production Deployment Guide

This guide walks you through deploying your Crumbs application to production using **100% free services**:

- **Frontend (Angular)**: Vercel (Free)
- **Backend (Django)**: Render (Free)
- **Database (PostgreSQL)**: Render PostgreSQL (Free)
- **Redis**: Render Redis (Free)
- **Celery Worker**: Render Background Worker (Free)

---

## Prerequisites

Before starting deployment, you must:

✅ **Complete Local PostgreSQL Migration**
- Follow `docs/LOCAL_POSTGRESQL_SETUP.md`
- Test your app locally with PostgreSQL
- Ensure all data is migrated and working

✅ **Have a GitHub Account**
- Your code must be pushed to GitHub
- Both Render and Vercel deploy from Git

✅ **Have Your Data Backup**
- Run `python scripts\backup_data.py`
- Keep the JSON file safe for production restore

---

## Part 1: Push Your Code to GitHub

### 1. Initialize Git (if not already done)

```bash
cd d:\Backup\Crumbs
git init
git add .
git commit -m "Prepare for production deployment"
```

### 2. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `crumbs` (or any name you prefer)
3. Visibility: **Private** (recommended) or Public
4. **Do NOT** initialize with README (you already have code)
5. Click **"Create repository"**

### 3. Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/crumbs.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

## Part 2: Deploy Backend to Render

### 1. Create Render Account

1. Go to https://render.com/
2. Click **"Get Started for Free"**
3. Sign up with GitHub (easiest - auto-connects repos)

### 2. Create New Blueprint

1. From Render Dashboard, click **"New +"** → **"Blueprint"**
2. Connect your GitHub repository (`crumbs`)
3. Render will detect `render.yaml` automatically
4. Click **"Apply"**

This will create:
- ✅ PostgreSQL Database (`crumbs-db`)
- ✅ Redis Instance (`crumbs-redis`)
- ✅ Web Service (`crumbs-backend`)
- ✅ Background Worker (`crumbs-celery-worker`)

### 3. Wait for Initial Build

- All services will start building (5-10 minutes)
- **Don't worry if they fail initially** - we need to set environment variables

### 4. Configure Environment Variables

#### For `crumbs-backend` Web Service:

1. Click on **"crumbs-backend"** service
2. Go to **"Environment"** tab
3. Add these variables:

```env
DEBUG=False

# Generate a new secret key (run this command locally):
# python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
DJANGO_SECRET_KEY=paste-generated-key-here

# This will be your Render URL (update after first deploy)
ALLOWED_HOSTS=crumbs-backend.onrender.com,crumbs-backend-YOURCODE.onrender.com

# Frontend URL (we'll update this after deploying to Vercel)
FRONTEND_URL=https://crumbs.vercel.app
CORS_ALLOWED_ORIGINS=https://crumbs.vercel.app
CSRF_TRUSTED_ORIGINS=https://crumbs.vercel.app

# Email (optional - for password resets)
USE_REAL_EMAIL=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=noreply@crumbs.com

# Payment Gateway (add when ready)
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
RAZORPAY_WEBHOOK_SECRET=
```

**Important Notes:**
- `DATABASE_URL`, `REDIS_URL`, `CELERY_BROKER_URL` are **auto-set** by render.yaml
- For Gmail, use **App Password**: https://support.google.com/accounts/answer/185833
- Generate SECRET_KEY locally, never use the default!

4. Click **"Save Changes"**

#### For `crumbs-celery-worker` Background Worker:

1. Click on **"crumbs-celery-worker"** service
2. Go to **"Environment"** tab
3. Add these variables:

```env
DEBUG=False
DJANGO_SECRET_KEY=same-key-as-backend
USE_REAL_EMAIL=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

4. Click **"Save Changes"**

### 5. Trigger Redeploy

1. Go to **"crumbs-backend"** service
2. Click **"Manual Deploy"** → **"Deploy latest commit"**
3. Wait for build to complete (3-5 minutes)

### 6. Check Backend URL

1. After successful deployment, find your backend URL:
   - Example: `https://crumbs-backend.onrender.com`
2. **Copy this URL** - you'll need it for the frontend

### 7. Run Migrations & Create Superuser

#### Option A: Using Render Shell (Recommended)

1. Go to **"crumbs-backend"** service
2. Click **"Shell"** tab (top right)
3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```
   Enter username, email, and password.

#### Option B: SSH Access

```bash
# Get SSH command from Render dashboard
render ssh crumbs-backend
python manage.py migrate
python manage.py createsuperuser
```

### 8. Restore Your Data to Production

You have two options:

#### Option A: Restore from Backup (Fastest)

1. Upload your backup JSON file to GitHub:
   ```bash
   # Locally
   git add backend/backups/database_backup_*.json
   git commit -m "Add production data backup"
   git push
   ```

2. In Render Shell:
   ```bash
   python scripts/restore_data.py backups/database_backup_YOURFILE.json
   ```

#### Option B: Use Management Command

If you have your catalog import command:

1. Upload product images (see "Media Files" section below)
2. In Render Shell:
   ```bash
   python manage.py import_catalog_data
   ```

### 9. Update ALLOWED_HOSTS

1. Note your exact Render URL (e.g., `crumbs-backend-xyz123.onrender.com`)
2. Go back to Environment variables
3. Update `ALLOWED_HOSTS`:
   ```
   ALLOWED_HOSTS=crumbs-backend-xyz123.onrender.com
   ```
4. Save and redeploy if needed

### 10. Test Backend

Visit: `https://your-backend.onrender.com/api/catalog/categories/`

You should see your categories in JSON format.

---

## Part 3: Deploy Frontend to Vercel

### 1. Create Vercel Account

1. Go to https://vercel.com/
2. Click **"Sign Up"**
3. Sign up with GitHub (easiest)

### 2. Import Project

1. From Vercel Dashboard, click **"Add New..."** → **"Project"**
2. Find your `crumbs` repository
3. Click **"Import"**

### 3. Configure Project

**Framework Preset**: Angular (should auto-detect)

**Root Directory**: Click **"Edit"** → Select `frontend`

**Build Settings**:
- Build Command: `npm run build` (auto-detected)
- Output Directory: `dist/angular-project/browser` (auto-detected from vercel.json)

**Environment Variables**: 
Add these if your Angular app uses them:
```
BACKEND_API_URL=https://your-backend.onrender.com
```

### 4. Deploy

1. Click **"Deploy"**
2. Wait 2-3 minutes for build
3. You'll get a URL like: `https://crumbs-xyz123.vercel.app`

### 5. Update Angular API URL

#### If you have environment files:

1. Update `frontend/src/environments/environment.prod.ts`:
   ```typescript
   export const environment = {
     production: true,
     apiUrl: 'https://your-backend.onrender.com/api'
   };
   ```

2. Commit and push:
   ```bash
   git add frontend/src/environments/
   git commit -m "Update production API URL"
   git push
   ```

3. Vercel will auto-deploy the update

#### If you have hardcoded URLs:

Search your Angular code for `localhost:8000` and replace with your Render backend URL.

### 6. Update Backend CORS Settings

1. Go back to Render → `crumbs-backend` → Environment
2. Update these variables with your Vercel URL:
   ```
   FRONTEND_URL=https://your-app.vercel.app
   CORS_ALLOWED_ORIGINS=https://your-app.vercel.app
   CSRF_TRUSTED_ORIGINS=https://your-app.vercel.app
   ```
3. Save Changes (auto-redeploys)

### 7. Custom Domain (Optional)

#### For Vercel (Frontend):
1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

#### For Render (Backend):
1. Go to `crumbs-backend` → Settings → Custom Domain
2. Add domain (e.g., `api.yourdomain.com`)
3. Update CORS settings with custom domain

---

## Part 4: Handle Media Files (Product Images)

### Problem:
Your product images are in `backend/media/` but Render's free tier has **ephemeral storage** - files uploaded at runtime get deleted on restart.

### Solutions:

#### Option A: Store Media in Git (Simple, Works for Small Projects)

**If your media folder is small (<100MB)**:

1. Update `.gitignore` to allow media:
   ```
   # Comment out or remove this line from backend/.gitignore:
   # media/
   ```

2. Commit media files:
   ```bash
   git add backend/media/
   git commit -m "Add product images"
   git push
   ```

3. Images will be deployed with your code

**Limitations**: 
- Only for static product images that don't change
- User-uploaded images still won't persist

#### Option B: Use Cloudinary (Free Tier - Recommended for Production)

**Free Tier**: 25GB storage, 25GB bandwidth/month

1. Sign up at https://cloudinary.com/
2. Install in backend:
   ```bash
   pip install django-cloudinary-storage
   ```

3. Update `requirements.txt`:
   ```
   django-cloudinary-storage==0.3.0
   ```

4. Configure in `settings.py`:
   ```python
   INSTALLED_APPS = [
       # ...
       'cloudinary_storage',
       'cloudinary',
   ]

   # Cloudinary settings
   CLOUDINARY_STORAGE = {
       'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
       'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
       'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
   }

   DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
   ```

5. Add Cloudinary credentials to Render environment variables

6. Upload existing images to Cloudinary

#### Option C: AWS S3 Free Tier

Similar to Cloudinary but requires more setup. Good if you want to learn AWS.

#### Option D: Accept Image Loss (Development/Demo)

If this is just for demo/portfolio:
- Product images reset on deployment (not ideal but works)
- Focus on functionality over persistence

---

## Part 5: Monitoring & Maintenance

### Check Service Status

**Render Dashboard**: Shows all service health
- Green = Running
- Yellow = Building
- Red = Failed

**Free Tier Limitations**:
- Services spin down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds (cold start)
- 750 hours/month per service (enough for 1 app running 24/7)

### View Logs

**Backend Logs**:
1. Render → `crumbs-backend` → Logs tab
2. See real-time application logs

**Celery Worker Logs**:
1. Render → `crumbs-celery-worker` → Logs tab
2. See async task processing

**Frontend Logs**:
1. Vercel → Project → Deployments → Click deployment → View logs

### Database Management

**Access PostgreSQL**:

1. Render → `crumbs-db` → Connect tab
2. Copy connection string
3. Use with any PostgreSQL client (pgAdmin, DBeaver, etc.)

**Backup Database**:

```bash
# From Render Shell
python scripts/backup_data.py
# Download the backup file
```

Or use PostgreSQL dump:
```bash
pg_dump DATABASE_URL > backup.sql
```

### Update Application

**Backend/Frontend Updates**:
1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update feature X"
   git push
   ```
3. Render and Vercel **auto-deploy** from GitHub
4. Check logs to confirm successful deployment

---

## Troubleshooting

### Backend Issues

#### Error: "Application failed to respond"
**Solutions**:
- Check Render logs for errors
- Verify `ALLOWED_HOSTS` includes your Render URL
- Ensure migrations ran successfully
- Check DATABASE_URL is set

#### Error: "ModuleNotFoundError"
**Solutions**:
- Check all dependencies in `requirements.txt`
- Verify build completed successfully
- Manual redeploy

#### Error: "CORS error" from frontend
**Solutions**:
- Verify `CORS_ALLOWED_ORIGINS` includes your Vercel URL
- Check `CSRF_TRUSTED_ORIGINS` as well
- Use exact URL (with https://)

### Frontend Issues

#### Error: "Failed to fetch from API"
**Solutions**:
- Check backend URL in environment files
- Verify backend is running (visit API URL directly)
- Check browser console for CORS errors

#### Images not loading
**Solutions**:
- Check media files are in Git or Cloudinary
- Verify MEDIA_URL settings
- Check image paths in Angular code

### Database Issues

#### Error: "Too many connections"
**Solutions**:
- Free tier has connection limits
- Check for unclosed connections
- Use connection pooling (already configured)

#### Data not showing
**Solutions**:
- Verify migrations ran: `python manage.py showmigrations`
- Check if data restore completed
- Query database directly to confirm data exists

### Celery Worker Issues

#### Async tasks not processing
**Solutions**:
- Check `crumbs-celery-worker` is running
- Verify Redis connection
- Check worker logs for errors
- Ensure CELERY_BROKER_URL is set

---

## Cost Breakdown (FREE!)

| Service | Free Tier | Limits |
|---------|-----------|--------|
| **Render PostgreSQL** | Free | 0.5 GB storage |
| **Render Redis** | Free | 25 MB |
| **Render Web Service** | Free | 750 hrs/month |
| **Render Worker** | Free | 750 hrs/month |
| **Vercel** | Free | Unlimited sites, 100GB bandwidth |
| **Total** | **$0/month** | Perfect for small projects! |

**When to Upgrade**:
- More than 0.5GB database → $7/month PostgreSQL
- Need always-on (no cold starts) → $7/month instance
- High traffic (>100GB bandwidth) → Vercel Pro $20/month

---

## Security Checklist

Before going live, verify:

- [ ] `DEBUG=False` in production
- [ ] Strong `DJANGO_SECRET_KEY` (generated, not default)
- [ ] `ALLOWED_HOSTS` restricted to your domains
- [ ] `CORS_ALLOWED_ORIGINS` restricted to your frontend domain
- [ ] Database credentials not in code (use environment variables)
- [ ] Gmail app password used (not regular password)
- [ ] Razorpay test keys for testing, live keys for production
- [ ] HTTPS enabled (automatic on Render/Vercel)
- [ ] Admin panel accessible only to you

---

## Performance Tips

### Backend (Render)

1. **Enable WhiteNoise** (already configured) - serves static files faster
2. **Use Redis caching** - cache API responses:
   ```python
   from django.views.decorators.cache import cache_page
   
   @cache_page(60 * 15)  # Cache for 15 minutes
   def product_list(request):
       ...
   ```
3. **Database indexes** - add indexes to frequently queried fields
4. **Query optimization** - use `select_related()` and `prefetch_related()`

### Frontend (Vercel)

1. **Lazy loading** - load modules on demand
2. **Image optimization** - compress product images
3. **Caching** - leverage browser caching (already in vercel.json)
4. **AOT compilation** - already enabled in production build

---

## Next Steps

✅ Your app is now live and free!

**Share Your App**:
- Frontend: `https://your-app.vercel.app`
- Backend API: `https://your-backend.onrender.com/api/`
- Admin: `https://your-backend.onrender.com/admin/`

**Monitor Usage**:
- Check Render dashboard for resource usage
- Monitor Vercel bandwidth
- Watch for errors in logs

**Iterate**:
- Add features
- Fix bugs
- Scale when needed

---

## Common Commands Reference

### Local Development
```bash
# Start backend
cd backend
python manage.py runserver

# Start frontend
cd frontend
npm start

# Backup data
python scripts/backup_data.py

# Restore data
python scripts/restore_data.py backups/file.json
```

### Production (Render Shell)
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --no-input

# Check deployment
python manage.py check --deploy

# Access Django shell
python manage.py shell
```

### Git Deployment
```bash
# Deploy updates
git add .
git commit -m "Update message"
git push  # Auto-deploys to Render & Vercel
```

---

## Support & Resources

**Render Documentation**: https://render.com/docs
**Vercel Documentation**: https://vercel.com/docs
**Django Deployment**: https://docs.djangoproject.com/en/stable/howto/deployment/

**Need Help?**
- Check logs first (Render/Vercel dashboards)
- Review this guide's Troubleshooting section
- Search Render/Vercel community forums
- Check GitHub issues for your dependencies

---

**Congratulations! Your application is now live on production! 🎉**
