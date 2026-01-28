import os
import tarfile
import shutil
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    """
    python manage.py restore_media --file /path/to/your/backups/wagtail_media_2025-12-22_120000.tar.gz
    """
    help = 'Restores Wagtail media from a .tar.gz backup file'

    def add_arguments(self, parser):
        # Adding the --file argument as requested
        parser.add_argument(
            '--file', 
            type=str, 
            help='Path to the .tar.gz backup file',
            required=True
        )

    def handle(self, *args, **options):
        file_path = options['file']
        target_dir = settings.MEDIA_ROOT

        # 1. Validation
        if not os.path.exists(file_path):
            raise CommandError(f"Backup file not found at: {file_path}")

        if not tarfile.is_tarfile(file_path):
            raise CommandError(f"File is not a valid tar archive: {file_path}")

        self.stdout.write(self.style.WARNING(f"Restoring media to: {target_dir}"))
        
        # 2. Safety: Handle existing media directory
        if os.path.exists(target_dir):
            # You might want to back up or clear the current media to avoid conflicts
            self.stdout.write("Existing media directory found. Cleaning up before restore...")
            shutil.rmtree(target_dir)
        
        os.makedirs(target_dir, exist_ok=True)

        # 3. Extraction
        try:
            with tarfile.open(file_path, "r:gz") as tar:
                # We extract to the PARENT of MEDIA_ROOT because the archive 
                # contains the 'media' folder itself
                extract_path = os.path.dirname(target_dir)
                
                self.stdout.write(f"Extracting {file_path}...")
                tar.extractall(path=extract_path)
            
            self.stdout.write(self.style.SUCCESS(f"Successfully restored media from {file_path}"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Restore failed: {str(e)}"))