# Simple Data Migration - SQLite to Production PostgreSQL

**Quick Guide**: Keep SQLite locally, migrate data directly to production.

---

## What You'll Do

1. ✅ Export SQLite data to JSON (1 command)
2. ✅ Keep using SQLite for development (no changes)
3. ✅ Deploy to Render (PostgreSQL auto-created)
4. ✅ Import JSON data to production (1 command in Render shell)

**No local PostgreSQL installation needed!**

---

## Step 1: Export Your Data (Local)

```cmd
cd d:\Backup\Crumbs\backend
python scripts\backup_data.py
```

**Result**: `backend/backups/database_backup_YYYYMMDD_HHMMSS.json`

This file contains **all your data**: products, categories, users, orders, everything!

---

## Step 2: Continue Using SQLite Locally

**Nothing changes!** Your `.env` stays the same:

```env
DEBUG=True
DJANGO_SECRET_KEY=your-local-key
# No database settings = SQLite by default
```

Keep developing normally:
```cmd
python manage.py runserver
```

---

## Step 3: Push to GitHub

```bash
git add .
git commit -m "Add deployment configs and data backup"
git push
```

Your backup JSON goes to GitHub (it's in `backend/backups/`).

---

## Step 4: Deploy to Render

Follow `DEPLOYMENT_GUIDE.md` to:
1. Create Render account
2. Deploy using `render.yaml` (creates PostgreSQL automatically)
3. Configure environment variables
4. Wait for deployment

---

## Step 5: Import Data to Production

### Option A: Via Render Shell (Easiest)

1. Go to Render Dashboard → `crumbs-backend`
2. Click **"Shell"** tab
3. Run migrations first:
   ```bash
   python manage.py migrate
   ```

4. Import your data:
   ```bash
   python scripts/restore_data.py backups/database_backup_YYYYMMDD_HHMMSS.json
   ```

5. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

### Option B: Via SSH

```bash
# Get SSH command from Render
render ssh crumbs-backend

# Then run:
python manage.py migrate
python scripts/restore_data.py backups/database_backup_YYYYMMDD_HHMMSS.json
python manage.py createsuperuser
```

---

## Step 6: Verify Production Data

Visit your production API:
```
https://your-backend.onrender.com/api/catalog/categories/
```

You should see all your products and categories! 🎉

---

## How It Works

### Development (Local)

```
SQLite (db.sqlite3) ← Your current setup
↓
No changes needed!
```

### Production (Render)

```
Render sets DATABASE_URL → Django uses PostgreSQL
↓
You import your data → All data available in production
```

### The Magic

In `settings.py` (already configured):

```python
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Production: PostgreSQL from Render
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
else:
    # Development: SQLite
    DATABASES = {'default': {'ENGINE': 'sqlite3', ...}}
```

---

## Important Notes

### ✅ Advantages

- **Simple**: No local PostgreSQL setup needed
- **Fast**: Direct migration to production
- **Safe**: Local development unchanged

### ⚠️ Considerations

- **First deploy**: Must import data manually (one-time)
- **Updates**: Future data changes need re-export/import
- **Testing**: Can't test PostgreSQL locally (usually fine)

### 🔄 Ongoing Data Sync

If you add products locally and want them in production:

1. **Export again**:
   ```cmd
   python scripts\backup_data.py
   ```

2. **Push to GitHub**:
   ```bash
   git add backend/backups/
   git commit -m "Update product data"
   git push
   ```

3. **Import to production**:
   ```bash
   # In Render shell
   python scripts/restore_data.py backups/database_backup_NEW.json
   ```

**Better approach for ongoing changes**:
- Add products via production admin panel
- Or use your catalog import management command
- Or consider local PostgreSQL if frequent sync needed

---

## FAQ

### Q: Will this delete my local SQLite database?

**A:** No! The backup script only reads from SQLite. Your local data is safe.

### Q: Can I test PostgreSQL before production?

**A:** Yes, but you'd need to install PostgreSQL locally (see `LOCAL_POSTGRESQL_SETUP.md`). For most cases, testing directly in production is fine.

### Q: What if import fails in production?

**A:** Common fixes:
- Ensure migrations ran first: `python manage.py migrate`
- Check backup file is valid JSON
- Drop and recreate database if needed (via Render dashboard)

### Q: How do I handle media files (images)?

**A:** Media files aren't in the database. Options:
- Commit to Git (if small)
- Use Cloudinary (recommended)
- Upload via admin panel in production

See deployment guide for details.

### Q: Can I switch back to local SQLite?

**A:** Yes! Local development is always SQLite unless you set `DATABASE_URL`.

---

## Troubleshooting

### Backup fails locally

```cmd
# Make sure you're in backend directory
cd d:\Backup\Crumbs\backend

# Activate venv if needed
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Try again
python scripts\backup_data.py
```

### Import fails in production

```bash
# Check migrations ran
python manage.py showmigrations

# If not, run them
python manage.py migrate

# Try import again
python scripts/restore_data.py backups/your_file.json
```

### Data shows in API but not admin

```bash
# Create superuser
python manage.py createsuperuser
```

---

## Quick Command Reference

### Local (Windows)
```cmd
# Export data
cd backend
python scripts\backup_data.py

# Check backup created
dir backups
```

### Production (Render Shell)
```bash
# Import data
python manage.py migrate
python scripts/restore_data.py backups/database_backup_YYYYMMDD_HHMMSS.json
python manage.py createsuperuser
```

---

## Next Steps

1. ✅ Export your data: `python scripts\backup_data.py`
2. ✅ Push to GitHub
3. ✅ Follow `DEPLOYMENT_GUIDE.md` to deploy
4. ✅ Import data in Render shell

**That's it!** Your data will be live in production. 🚀
