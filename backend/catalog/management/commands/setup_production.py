"""
Management command to set up production database with data.
This runs automatically after migrations during deployment.
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from pathlib import Path
import os


class Command(BaseCommand):
    help = 'Set up production database with initial data'

    def handle(self, *args, **options):
        # Only run in production (when DATABASE_URL is set)
        if not os.environ.get('DATABASE_URL'):
            self.stdout.write(self.style.WARNING('Skipping: Not in production environment'))
            return

        # Check if data already exists
        from catalog.models import Category
        if Category.objects.exists():
            self.stdout.write(self.style.SUCCESS('Data already exists, skipping import'))
            return

        self.stdout.write(self.style.SUCCESS('Setting up production database...'))

        # Find the backup file
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        backup_dir = base_dir / 'backups'
        
        if backup_dir.exists():
            backups = list(backup_dir.glob('database_backup_*.json'))
            if backups:
                # Use the most recent backup
                latest_backup = max(backups, key=lambda p: p.stat().st_mtime)
                self.stdout.write(f'Importing data from: {latest_backup.name}')
                
                try:
                    # Import the data
                    call_command('loaddata', str(latest_backup), verbosity=2)
                    self.stdout.write(self.style.SUCCESS('✓ Data imported successfully!'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to import data: {str(e)}'))
            else:
                self.stdout.write(self.style.WARNING('No backup files found'))
        else:
            self.stdout.write(self.style.WARNING('Backups directory not found'))
