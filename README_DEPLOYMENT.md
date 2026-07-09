# 🚀 Crumbs - Free Hosting Deployment

Your complete guide to deploying the Crumbs application to production **for FREE**.

---

## 📋 Quick Overview

This project is now ready for production deployment using:

- **Frontend**: Angular → Vercel (Free)
- **Backend**: Django → Render (Free)
- **Database**: PostgreSQL → Render (Free)
- **Cache/Queue**: Redis → Render (Free)
- **Worker**: Celery → Render (Free)

**Total Cost: $0/month** ✨

---

## 🎯 Two Approaches Available

### Approach 1: Simple Migration (Recommended) ⭐

- ✅ **Keep SQLite for local development** (no changes)
- ✅ **Use PostgreSQL only in production**
- ✅ **Export data → Deploy → Import to production**
- ✅ **No local PostgreSQL installation needed**

**📖 Follow**: `docs/DATA_MIGRATION_SIMPLE.md`

### Approach 2: Full Local Testing

- Install PostgreSQL locally
- Test with PostgreSQL before deploying
- More setup, but can test everything locally

**📖 Follow**: `docs/LOCAL_POSTGRESQL_SETUP.md`

---

## 🚀 Quick Start (Simple Approach)

### Step 1: Export Your Data (1 minute)

```bash
cd backend
python scripts\backup_data.py
```

**Result**: Your data is exported to `backend/backups/database_backup_*.json`

### Step 2: Keep Developing Locally

**Nothing changes!** Continue using SQLite:

```bash
python manage.py runserver
```

### Step 3: Deploy to Production (15 minutes)

1. Push code to GitHub
2. Deploy to Render (backend) - **PostgreSQL created automatically**
3. Deploy to Vercel (frontend)
4. Import your data in Render shell

**Detailed steps**: See `docs/DEPLOYMENT_GUIDE.md`

---

## 📚 Complete Documentation

### For Quick/Simple Migration ⭐

1. **[Simple Data Migration](docs/DATA_MIGRATION_SIMPLE.md)** 
   - Keep SQLite locally
   - Export → Deploy → Import
   - **Start here!**

2. **[Production Deployment Guide](docs/DEPLOYMENT_GUIDE.md)** 
   - Deploy to Render + Vercel
   - Configure environment variables
   - Import data to production

### For Full Local Testing

1. **[Local PostgreSQL Setup](docs/LOCAL_POSTGRESQL_SETUP.md)**
   - Install PostgreSQL on Windows
   - Test locally before deploying

---

## 📁 Project Structure

```
Crumbs/
├── backend/                    # Django REST API
│   ├── main/                  # Django settings
│   ├── accounts/              # User authentication
│   ├── catalog/               # Products catalog
│   ├── orders/                # Order management
│   ├── scripts/               # Deployment scripts
│   │   ├── backup_data.py    # Export SQLite data
│   │   └── restore_data.py   # Import to PostgreSQL
│   ├── requirements.txt       # Python dependencies
│   ├── render.yaml           # Render deployment config
│   └── .env.production.example
│
├── frontend/                  # Angular SPA
│   ├── src/                  # Angular source code
│   ├── vercel.json           # Vercel deployment config
│   └── package.json
│
└── docs/                      # Documentation
    ├── LOCAL_POSTGRESQL_SETUP.md
    └── DEPLOYMENT_GUIDE.md
```

---

## 🛠️ Key Files Added for Deployment

### Backend
- ✅ `scripts/backup_data.py` - Backup SQLite data
- ✅ `scripts/restore_data.py` - Restore to PostgreSQL
- ✅ `render.yaml` - Render deployment configuration
- ✅ `.env.production.example` - Environment variables template
- ✅ `.slugignore` - Files to exclude from deployment
- ✅ Updated `requirements.txt` - Added PostgreSQL support

### Frontend
- ✅ `vercel.json` - Vercel deployment configuration
- ✅ `.gitignore` - Updated for deployment

### Settings Updates
- ✅ PostgreSQL support with `DATABASE_URL`
- ✅ WhiteNoise for static files
- ✅ Production security settings
- ✅ CORS configuration
- ✅ Redis caching configuration

---

## 🔧 Configuration Files

### Backend Environment Variables

See `.env.production.example` for all required variables.

**Key Variables**:
- `DEBUG=False`
- `DJANGO_SECRET_KEY` - Generate new for production
- `DATABASE_URL` - Auto-set by Render
- `REDIS_URL` - Auto-set by Render
- `ALLOWED_HOSTS` - Your Render domain
- `CORS_ALLOWED_ORIGINS` - Your Vercel domain
- `FRONTEND_URL` - Your Vercel domain

### Frontend Configuration

Update `frontend/src/environments/environment.prod.ts`:
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://your-backend.onrender.com/api'
};
```

---

## 📊 Free Tier Limits

| Service | Limit | Notes |
|---------|-------|-------|
| Render PostgreSQL | 0.5 GB | Enough for small-medium apps |
| Render Redis | 25 MB | Sufficient for caching/Celery |
| Render Web Service | 750 hrs/month | Runs 24/7 for 1 app |
| Render Worker | 750 hrs/month | For Celery background tasks |
| Vercel | 100 GB bandwidth | Plenty for most sites |

**Perfect for**: Personal projects, portfolios, small businesses, MVPs

---

## 🚨 Important Notes

### 1. Cold Starts
Free tier services spin down after 15 minutes of inactivity. First request takes ~30 seconds to wake up.

### 2. Media Files
Render has ephemeral storage. For persistent media:
- **Option A**: Store in Git (small projects)
- **Option B**: Use Cloudinary (recommended)
- **Option C**: Use AWS S3

See deployment guide for details.

### 3. Email Configuration
For password reset emails:
- Use Gmail with **App Password** (not regular password)
- Or use SendGrid free tier (100 emails/day)

### 4. Database Backups
Render doesn't auto-backup free databases. Schedule regular backups:
```bash
python scripts/backup_data.py
```

---

## 🔐 Security Checklist

Before deploying to production:

- [ ] Generate new `DJANGO_SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Restrict `CORS_ALLOWED_ORIGINS` to your frontend
- [ ] Use environment variables (never commit secrets)
- [ ] Enable HTTPS (automatic on Render/Vercel)
- [ ] Use Gmail App Password (not regular password)
- [ ] Review Django security settings

---

## 🐛 Troubleshooting

### Backend Not Working?
1. Check Render logs
2. Verify environment variables
3. Ensure migrations ran
4. Check database connection

### Frontend Can't Connect?
1. Verify backend URL in environment files
2. Check CORS settings in backend
3. Ensure backend is running

### Data Not Showing?
1. Did you restore the database backup?
2. Check migrations: `python manage.py showmigrations`
3. Query database directly

**Full troubleshooting**: See [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md#troubleshooting)

---

## 📞 Support

**Documentation**:
- [Local PostgreSQL Setup](docs/LOCAL_POSTGRESQL_SETUP.md)
- [Production Deployment](docs/DEPLOYMENT_GUIDE.md)

**External Resources**:
- [Render Docs](https://render.com/docs)
- [Vercel Docs](https://vercel.com/docs)
- [Django Deployment](https://docs.djangoproject.com/en/stable/howto/deployment/)

---

## 🎯 Deployment Checklist

### Local Setup ✅
- [ ] Install PostgreSQL
- [ ] Backup SQLite data (`python scripts\backup_data.py`)
- [ ] Configure PostgreSQL in `.env`
- [ ] Run migrations (`python manage.py migrate`)
- [ ] Restore data (`python scripts\restore_data.py`)
- [ ] Test locally (Django + Angular)

### Production Deployment 🚀
- [ ] Push code to GitHub
- [ ] Create Render account
- [ ] Deploy using `render.yaml` blueprint
- [ ] Configure environment variables
- [ ] Run migrations in Render shell
- [ ] Create superuser
- [ ] Restore data to production
- [ ] Deploy frontend to Vercel
- [ ] Update backend CORS settings
- [ ] Test production site

### Post-Deployment ✨
- [ ] Test all features
- [ ] Check admin panel
- [ ] Verify API endpoints
- [ ] Test authentication
- [ ] Verify email sending (if enabled)
- [ ] Monitor logs for errors
- [ ] Set up custom domain (optional)

---

## 📈 Next Steps

Once deployed:

1. **Monitor** - Check Render/Vercel dashboards regularly
2. **Optimize** - Add caching, compress images
3. **Scale** - Upgrade if you hit free tier limits
4. **Iterate** - Keep improving your app

---

## 🎉 Success!

Once everything is deployed:

- **Frontend**: `https://your-app.vercel.app`
- **Backend API**: `https://your-backend.onrender.com/api/`
- **Admin Panel**: `https://your-backend.onrender.com/admin/`

Share your app with the world! 🌍

---

**Made with ❤️ using Django, Angular, and free hosting**
