"""
Script to backup all data from SQLite database to JSON format.
Run this before migrating to PostgreSQL to preserve all your data.

Usage:
    python scripts/backup_data.py
"""

import os
import sys
import django
from pathlib import Path
from datetime import datetime

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SECRET_KEY', 'temporary-key-for-backup')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from django.core.management import call_command


def backup_database():
    """Create a backup of all database data to JSON file."""
    
    # Create backups directory if it doesn't exist
    backup_dir = BASE_DIR / 'backups'
    backup_dir.mkdir(exist_ok=True)
    
    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = backup_dir / f'database_backup_{timestamp}.json'
    
    print("=" * 60)
    print("DATABASE BACKUP SCRIPT")
    print("=" * 60)
    print(f"\nBacking up database to: {backup_file}")
    print("\nThis may take a few minutes depending on data size...")
    
    try:
        # Export all data using Django's dumpdata command
        with open(backup_file, 'w', encoding='utf-8') as f:
            call_command(
                'dumpdata',
                '--natural-foreign',
                '--natural-primary',
                '--indent', '2',
                exclude=[
                    'contenttypes',
                    'auth.permission',
                    'sessions.session',
                    'admin.logentry',
                ],
                stdout=f
            )
        
        print(f"\n✓ SUCCESS! Database backed up successfully!")
        print(f"\nBackup file: {backup_file}")
        print(f"File size: {backup_file.stat().st_size / 1024:.2f} KB")
        print("\n" + "=" * 60)
        print("IMPORTANT: Keep this file safe!")
        print("You'll need it to restore data to PostgreSQL.")
        print("=" * 60)
        
        return str(backup_file)
        
    except Exception as e:
        print(f"\n✗ ERROR: Backup failed!")
        print(f"Error details: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    backup_database()
