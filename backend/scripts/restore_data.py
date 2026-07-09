"""
Script to restore data from JSON backup to PostgreSQL database.
Run this after setting up PostgreSQL and running migrations.

Usage:
    python scripts/restore_data.py <backup_file.json>
    
Example:
    python scripts/restore_data.py backups/database_backup_20260709_120000.json
"""

import os
import sys
import django
from pathlib import Path

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from django.core.management import call_command


def restore_database(backup_file):
    """Restore data from JSON backup file to current database."""
    
    backup_path = Path(backup_file)
    
    if not backup_path.exists():
        print(f"✗ ERROR: Backup file not found: {backup_file}")
        print("\nAvailable backups:")
        backup_dir = BASE_DIR / 'backups'
        if backup_dir.exists():
            backups = list(backup_dir.glob('*.json'))
            if backups:
                for b in sorted(backups, reverse=True):
                    print(f"  - {b.name}")
            else:
                print("  No backup files found!")
        sys.exit(1)
    
    print("=" * 60)
    print("DATABASE RESTORE SCRIPT")
    print("=" * 60)
    print(f"\nRestoring from: {backup_file}")
    
    # Confirmation prompt
    print("\n⚠️  WARNING: This will add data to the current database.")
    print("Make sure you've already run migrations!")
    response = input("\nContinue? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("Restore cancelled.")
        sys.exit(0)
    
    print("\nRestoring data...")
    print("This may take a few minutes depending on data size...\n")
    
    try:
        # Load data using Django's loaddata command
        call_command('loaddata', str(backup_path), verbosity=2)
        
        print("\n" + "=" * 60)
        print("✓ SUCCESS! Data restored successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Test your application locally")
        print("2. Verify all data is present")
        print("3. Check admin panel and API endpoints")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ ERROR: Restore failed!")
        print(f"Error details: {str(e)}")
        print("\nCommon issues:")
        print("- Make sure you've run migrations first: python manage.py migrate")
        print("- Check that PostgreSQL is running and configured correctly")
        print("- Verify .env file has correct database settings")
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scripts/restore_data.py <backup_file.json>")
        print("\nExample:")
        print("  python scripts/restore_data.py backups/database_backup_20260709_120000.json")
        
        # Show available backups
        backup_dir = BASE_DIR / 'backups'
        if backup_dir.exists():
            backups = list(backup_dir.glob('*.json'))
            if backups:
                print("\nAvailable backups:")
                for b in sorted(backups, reverse=True):
                    print(f"  - {b.name}")
        sys.exit(1)
    
    restore_database(sys.argv[1])
