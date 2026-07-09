# Data Migration Guide - SQLite to Production PostgreSQL

This guide shows you how to **keep SQLite for local development** but migrate your data to **PostgreSQL in production**.

**TL;DR**: You don't need to install PostgreSQL locally. We'll export your SQLite data and import it directly to production.

---

## Overview

- ✅ **Local Development**: Keep using SQLite (no changes needed)
- ✅ **Production**: Use PostgreSQL on Render
- ✅ **Data Migration**: Export from SQLite → Import to production PostgreSQL

---

## Step 1: Backup Your SQLite Data

## Step 1: Backup Your SQLite Data

**This is the most important step!** Your entire database will be exported to a JSON file.

### 1. Navigate to Backend Directory

```cmd
cd d:\Backup\Crumbs\backend
```

### 2. Activate Virtual Environment (if you use one)

```cmd
venv\Scripts\activate
```

### 3. Run Backup Script

```cmd
python scripts\backup_data.py
```

**Output**:
```
============================================================
DATABASE BACKUP SCRIPT
============================================================

Backing up database to: D:\Backup\Crumbs\backend\backups\database_backup_20260709_143022.json

This may take a few minutes depending on data size...

✓ SUCCESS! Database backed up successfully!

Backup file: D:\Backup\Crumbs\backend\backups\database_backup_20260709_143022.json
File size: 245.67 KB

============================================================
IMPORTANT: Keep this file safe!
You'll need it to restore data to PostgreSQL.
============================================================
```

### 4. Verify Backup File

Check that the file exists:
```cmd
dir backups
```

You should see: `database_backup_YYYYMMDD_HHMMSS.json`

**⚠️ IMPORTANT**: 
- Keep this file safe!
- We'll upload it to production later
- This contains ALL your data (products, categories, users, orders)

---

## Step 2: Keep Using SQLite Locally

**No changes needed!** Your local development continues exactly as before:

```cmd
# Start Django development server
python manage.py runserver
```

Your app still uses SQLite locally. The PostgreSQL support only activates in production when `DATABASE_URL` is set.

---

## Step 3: Deploy to Production (See DEPLOYMENT_GUIDE.md)

Once you have your backup:
1. Push code to GitHub
2. Deploy to Render (creates PostgreSQL automatically)
3. Upload your backup JSON file
4. Restore data in production

See **`docs/DEPLOYMENT_GUIDE.md`** for complete deployment steps.

---

## How It Works

### Local Development (SQLite)

Your `.env` file has NO database settings (or they're commented out):

```env
# Local development uses SQLite by default
DEBUG=True
DJANGO_SECRET_KEY=your-local-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

Django defaults to SQLite when no `DATABASE_URL` is provided.

### Production (PostgreSQL)

Render sets `DATABASE_URL` environment variable automatically:

```env
DATABASE_URL=postgres://user:pass@host:5432/db
DEBUG=False
# ... other production settings
```

Django detects `DATABASE_URL` and uses PostgreSQL instead.

### The Code (Already Set Up)

In `settings.py`:

```python
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Production: use PostgreSQL
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
else:
    # Development: use SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(BASE_DIR / 'db.sqlite3'),
        }
    }
```

---

## Testing Before Production (Optional)

If you want to test PostgreSQL locally before deploying:

### Option A: Use PostgreSQL Locally (Full Test)

See the original guide at `docs/LOCAL_POSTGRESQL_SETUP_FULL.md` (will create if needed).

### Option B: Use SQLite in Production (Not Recommended)

You could keep SQLite in production, but you'll lose data on restarts (ephemeral storage).

### Option C: Skip Local Testing (Recommended)

- Your backup script already validates data export works
- Production migration is straightforward
- Render provides easy database access for troubleshooting

---

## FAQ

### Q: Will my local SQLite database be affected?

**A:** No! The backup script only *reads* from SQLite. Your local database stays untouched.

### Q: Do I need to install PostgreSQL on my computer?

**A:** No! You only need PostgreSQL in production (Render provides it).

### Q: What if my backup fails?

**A:** Common issues:
- **Virtual environment not activated**: Activate first
- **Missing dependencies**: Run `pip install -r requirements.txt`
- **Database locked**: Close any apps using the database

### Q: Can I test the restore locally?

**A:** Yes, but you'd need to install PostgreSQL. For most cases, testing in production is faster and easier.

### Q: What gets backed up?

**A:** Everything:
- All products and categories
- User accounts and profiles
- Orders and transactions
- Custom app data

**What doesn't get backed up:**
- Media files (product images) - handled separately
- Session data (excluded intentionally)
- Admin logs (excluded intentionally)

### Q: How large will my backup be?

**A:** Typical sizes:
- Small site (100 products): ~50-100 KB
- Medium site (1000 products): ~500 KB - 1 MB
- Large site (10k+ products): ~5-10 MB

JSON is text-based, so it's readable but not the most compact.

---

## Next Steps

✅ **You've backed up your data!**

Now follow **`docs/DEPLOYMENT_GUIDE.md`** to:
1. Push your code to GitHub
2. Deploy to Render
3. Restore your data to production PostgreSQL
4. Deploy frontend to Vercel

---

## Backup Script Reference

### Create Backup
```cmd
python scripts\backup_data.py
```

### List Backups
```cmd
dir backups
```

### Backup Location
```
backend/backups/database_backup_YYYYMMDD_HHMMSS.json
```

### Restore in Production (Later)
```bash
# In Render shell (after deployment)
python scripts/restore_data.py backups/database_backup_YYYYMMDD_HHMMSS.json
```

---

## Troubleshooting

### Error: "scripts\backup_data.py not found"

**Solution**: Make sure you're in the `backend` directory:
```cmd
cd d:\Backup\Crumbs\backend
python scripts\backup_data.py
```

### Error: "ModuleNotFoundError: No module named 'django'"

**Solution**: Activate virtual environment or install dependencies:
```cmd
# If using venv
venv\Scripts\activate

# Then
pip install -r requirements.txt
```

### Error: "Unable to open database file"

**Solution**: 
- Make sure Django isn't running (`python manage.py runserver`)
- Close any database browser tools
- Check that `db.sqlite3` exists

### Backup File Too Large for Git

If your backup is over 100MB:
- Use Git LFS (Large File Storage)
- Or upload directly to Render (see deployment guide)
- Or use compressed format (gzip)

---

## Important Notes

📌 **Keep SQLite for Development**
- Faster setup
- Easier debugging
- No additional services needed

📌 **Use PostgreSQL in Production**
- Data persists across restarts
- Better performance for multiple users
- Standard for production Django apps

📌 **Backup Regularly**
- Before major changes
- Before deployments
- Weekly for active development

📌 **Test Restore Process**
- At least once in production
- Ensure backups are valid
- Practice disaster recovery

---

**Ready to deploy?** See **`docs/DEPLOYMENT_GUIDE.md`** for the next steps!

**Ready to deploy?** See **`docs/DEPLOYMENT_GUIDE.md`** for the next steps!
