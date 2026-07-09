# ⚡ Quick Start - Deploy with SQLite → PostgreSQL

**Goal**: Keep SQLite locally, deploy with PostgreSQL in production, migrate all your data.

---

## 3 Simple Steps

### 1️⃣ Export Your Data (30 seconds)

```cmd
cd backend
python scripts\backup_data.py
```

✅ Creates: `backend/backups/database_backup_YYYYMMDD_HHMMSS.json`  
✅ Contains: ALL your products, categories, users, orders

### 2️⃣ Deploy (15 minutes)

```bash
# Push to GitHub
git add .
git commit -m "Ready for deployment"
git push

# Then follow: docs/DEPLOYMENT_GUIDE.md
# - Deploy to Render (backend with PostgreSQL)
# - Deploy to Vercel (frontend)
```

### 3️⃣ Import Data to Production (2 minutes)

In Render Shell (after deployment):

```bash
# Run migrations
python manage.py migrate

# Import your data
python scripts/restore_data.py backups/database_backup_YYYYMMDD_HHMMSS.json

# Create admin user
python manage.py createsuperuser
```

**Done!** Your app is live with all your data! 🎉

---

## Your Local Setup (Unchanged)

```cmd
# Keep using SQLite locally
python manage.py runserver

# No PostgreSQL installation needed!
```

---

## How It Works

| Environment | Database | How |
|------------|----------|-----|
| **Local** | SQLite | Default (no env vars) |
| **Production** | PostgreSQL | Render sets `DATABASE_URL` |

Django automatically uses the right database based on environment!

---

## Next Steps

1. **Read**: `docs/DATA_MIGRATION_SIMPLE.md` - Detailed simple migration guide
2. **Or Read**: `docs/DEPLOYMENT_GUIDE.md` - Full deployment walkthrough
3. **Export data**: `python scripts\backup_data.py`
4. **Deploy**: Follow deployment guide
5. **Import**: In Render shell

---

## Need More Control?

Want to test PostgreSQL locally before production?  
→ Follow `docs/LOCAL_POSTGRESQL_SETUP.md` instead

---

**Cost**: $0/month | **Time**: ~20 minutes | **Difficulty**: Easy ✨
