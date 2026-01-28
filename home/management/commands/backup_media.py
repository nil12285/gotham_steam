import os
import tarfile
import boto3
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from botocore.exceptions import BotoCoreError, ClientError

class Command(BaseCommand):
    """
    Setup Cron
    0 0 * * 0 cd /path/to/your/project && .venv/bin/python manage.py backup_media
    """
    help = 'Backs up Wagtail media locally, and optionally uploads to OCI Object Storage'

    def handle(self, *args, **options):
        # 1. Setup Local Paths
        source_dir = settings.MEDIA_ROOT
        backup_base_dir = os.path.join(settings.BASE_DIR, 'backups')
        if not os.path.exists(backup_base_dir):
            os.makedirs(backup_base_dir)

        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        filename = f"wagtail_media_{timestamp}.tar.gz"
        local_path = os.path.join(backup_base_dir, filename)

        # 2. Create Local Backup (Always happens first)
        self.stdout.write(f"Creating local backup at {local_path}...")
        try:
            with tarfile.open(local_path, "w:gz") as tar:
                tar.add(source_dir, arcname=os.path.basename(source_dir))
            self.stdout.write(self.style.SUCCESS(f"Local backup created successfully."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Local compression failed: {str(e)}"))
            return

        # 3. Check for OCI Configurations
        oci_access_key = settings.OCI['ACCESS_KEY']
        oci_secret_key = settings.OCI['SECRET_KEY']
        oci_namespace = settings.OCI['NAMESPACE']
        oci_region = settings.OCI['REGION']
        oci_bucket = settings.OCI['BUCKET_NAME']

        if all([oci_access_key, oci_secret_key, oci_namespace, oci_region, oci_bucket]):
            self.stdout.write("OCI configuration found. Initiating upload...")
            
            endpoint = f"https://{oci_namespace}.compat.objectstorage.{oci_region}.oraclecloud.com"
            
            try:
                session = boto3.Session(
                    aws_access_key_id=oci_access_key,
                    aws_secret_access_key=oci_secret_key,
                    region_name=oci_region
                )
                s3 = session.client('s3', endpoint_url=endpoint)
                
                # Required for some OCI S3 compatibility regions
                extra_args = {'ACL': 'private'} 
                
                s3.upload_file(local_path, oci_bucket, filename, ExtraArgs=extra_args)
                self.stdout.write(self.style.SUCCESS(f"Successfully uploaded {filename} to OCI bucket '{oci_bucket}'"))
                
                # Optional: Uncomment the line below if you want to delete the local copy AFTER successful upload
                # os.remove(local_path)

            except (BotoCoreError, ClientError) as e:
                self.stdout.write(self.style.ERROR(f"OCI Upload failed: {str(e)}"))
        else:
            self.stdout.write(self.style.WARNING("OCI configuration missing. Skipping cloud upload. Local backup remains in /backups/"))

            