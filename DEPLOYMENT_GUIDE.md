# 🚀 Production Deployment Guide

## 📋 Overview

This guide covers deploying your Crumbs application to production. Choose the platform that best fits your needs.

---

## 🌟 Recommended Deployment Platforms

### 1. **Heroku** (Easiest)
- ✅ Easy to deploy
- ✅ Free tier available
- ✅ Managed PostgreSQL
- ✅ SSL included
- ⚠️ Can be expensive at scale

### 2. **DigitalOcean App Platform**
- ✅ Affordable
- ✅ Easy to use
- ✅ Good documentation
- ✅ Managed databases

### 3. **AWS / Google Cloud / Azure**
- ✅ Most scalable
- ✅ Most features
- ⚠️ More complex setup
- ⚠️ Steeper learning curve

### 4. **VPS (DigitalOcean Droplet / Linode)**
- ✅ Full control
- ✅ Affordable
- ⚠️ Requires server management skills
- ⚠️ You handle everything

---

## 🔧 Heroku Deployment (Recommended for Beginners)

### Step 1: Prepare Your Project

1. **Install Heroku CLI**:
   ```bash
   # Windows
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   
   # Mac
   brew tap heroku/brew && brew install heroku
   
   # Linux
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login to Heroku**:
   ```bash
   heroku login
   ```

3. **Create Procfile** (in project root):
   ```
   web: gunicorn main.wsgi --chdir backend
   ```

4. **Create runtime.txt** (in project root):
   ```
   python-3.12.0
   ```

5. **Update requirements.txt**:
   ```bash
   cd backend
   pip install gunicorn psycopg2-binary whitenoise
   pip freeze > requirements.txt
   ```

6. **Update settings.py** for Heroku:
   ```python
   # Add whitenoise for static files
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
       # ... rest of middleware
   ]
   
   # Static files
   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
   ```

### Step 2: Create Heroku App

```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:mini
```

### Step 3: Set Environment Variables

```bash
# Generate secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set variables
heroku config:set DJANGO_SECRET_KEY='your-generated-secret-key'
heroku config:set DEBUG=false
heroku config:set ALLOWED_HOSTS='your-app-name.herokuapp.com'
heroku config:set USE_REAL_EMAIL=true
heroku config:set EMAIL_HOST_USER='your-email@gmail.com'
heroku config:set EMAIL_HOST_PASSWORD='your-app-password'
heroku config:set FRONTEND_URL='https://your-frontend-url.com'
```

### Step 4: Deploy

```bash
git add .
git commit -m "Prepare for production"
git push heroku main

# Run migrations
heroku run python backend/manage.py migrate
heroku run python backend/manage.py createsuperuser
```

### Step 5: Deploy Frontend

1. **Build Angular app**:
   ```bash
   cd frontend
   ng build --configuration production
   ```

2. **Deploy to Netlify/Vercel**:
   - Create account on Netlify or Vercel
   - Connect your GitHub repo
   - Set build command: `cd frontend && ng build --configuration production`
   - Set publish directory: `frontend/dist/browser`
   - Set environment variable: `API_URL=https://your-app-name.herokuapp.com/api`

---

## 🐳 Docker Deployment

### Dockerfile (Backend)

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "main.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: crumbs_db
      POSTGRES_USER: crumbs_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: .
    command: gunicorn main.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./frontend/dist:/usr/share/nginx/html
    depends_on:
      - backend

volumes:
  postgres_data:
```

---

## 🖥️ VPS Deployment (Ubuntu 22.04)

### Step 1: Initial Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-dev libpq-dev nginx curl -y

# Install Node.js for frontend
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y
```

### Step 2: Setup Database

```bash
sudo -u postgres psql

CREATE DATABASE crumbs_db;
CREATE USER crumbs_user WITH PASSWORD 'secure_password';
ALTER ROLE crumbs_user SET client_encoding TO 'utf8';
ALTER ROLE crumbs_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE crumbs_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE crumbs_db TO crumbs_user;
\q
```

### Step 3: Setup Application

```bash
# Create app directory
sudo mkdir -p /var/www/crumbs
sudo chown $USER:$USER /var/www/crumbs
cd /var/www/crumbs

# Clone your repo
git clone your-repo-url .

# Setup Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
pip install gunicorn

# Create .env file
nano backend/.env
# Add your production environment variables

# Run migrations
cd backend
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### Step 4: Setup Gunicorn

Create `/etc/systemd/system/crumbs.service`:

```ini
[Unit]
Description=Crumbs Gunicorn Daemon
After=network.target

[Service]
User=your-username
Group=www-data
WorkingDirectory=/var/www/crumbs/backend
Environment="PATH=/var/www/crumbs/venv/bin"
ExecStart=/var/www/crumbs/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/crumbs/crumbs.sock \
          main.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start Gunicorn:
```bash
sudo systemctl start crumbs
sudo systemctl enable crumbs
```

### Step 5: Setup Nginx

Create `/etc/nginx/sites-available/crumbs`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/crumbs/backend/staticfiles/;
    }

    location /media/ {
        alias /var/www/crumbs/backend/media/;
    }

    location /api/ {
        proxy_pass http://unix:/var/www/crumbs/crumbs.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        root /var/www/crumbs/frontend/dist/browser;
        try_files $uri $uri/ /index.html;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/crumbs /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: Setup SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## 🔒 Security Checklist

After deployment, verify:

- [ ] HTTPS is working
- [ ] DEBUG=false
- [ ] SECRET_KEY is unique and secret
- [ ] Database credentials are secure
- [ ] Firewall is configured (only ports 80, 443, 22 open)
- [ ] SSH key authentication enabled (disable password auth)
- [ ] Regular backups configured
- [ ] Monitoring set up

---

## 📊 Monitoring & Maintenance

### Application Monitoring

1. **Sentry** (Error Tracking):
   ```bash
   pip install sentry-sdk
   ```
   
   Add to settings.py:
   ```python
   import sentry_sdk
   sentry_sdk.init(dsn="your-sentry-dsn")
   ```

2. **New Relic** (Performance):
   ```bash
   pip install newrelic
   newrelic-admin generate-config YOUR_LICENSE_KEY newrelic.ini
   ```

### Server Monitoring

- **Uptime monitoring**: UptimeRobot, Pingdom
- **Server metrics**: Datadog, Prometheus + Grafana
- **Log aggregation**: Papertrail, Loggly

---

## 🔄 CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{secrets.HEROKU_API_KEY}}
        heroku_app_name: "your-app-name"
        heroku_email: "your-email@example.com"
```

---

## 📞 Troubleshooting

### Common Issues

1. **500 Internal Server Error**
   - Check logs: `heroku logs --tail` or `sudo journalctl -u crumbs`
   - Verify all environment variables are set
   - Check DEBUG=false doesn't break anything

2. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check STATIC_ROOT and STATIC_URL settings
   - Verify Nginx is serving static files

3. **Database Connection Error**
   - Verify database credentials in .env
   - Check database is running
   - Test connection manually

4. **CORS Errors**
   - Update CORS_ALLOWED_ORIGINS
   - Update CSRF_TRUSTED_ORIGINS
   - Check frontend is using correct API URL

---

## ✅ Post-Deployment Checklist

- [ ] Site accessible via HTTPS
- [ ] Login/logout working
- [ ] Password reset emails being sent
- [ ] Protected routes require authentication
- [ ] Static files loading correctly
- [ ] Database migrations applied
- [ ] Admin panel accessible
- [ ] Error monitoring active
- [ ] Backups configured
- [ ] Domain DNS configured correctly

---

## 🎉 You're Live!

Your application is now running in production! 🚀

Monitor it regularly and keep dependencies updated for security patches.

**Need help?** Check the logs first, they'll tell you what's wrong!
