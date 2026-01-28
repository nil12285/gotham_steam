import os
import subprocess
from datetime import datetime
import boto3
from django.core.management.base import BaseCommand
from django.conf import settings
from botocore.exceptions import BotoCoreError, ClientError

class Command(BaseCommand):
    help = 'Backs up the database locally and uploads to OCI Object Storage'

    def handle(self, *args, **options):
        # 1. Setup Paths
        backup_base_dir = os.path.join(settings.BASE_DIR, 'backups')
        if not os.path.exists(backup_base_dir):
            os.makedirs(backup_base_dir)

        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        db_conf = settings.DATABASES['default']
        db_engine = db_conf['ENGINE']
        
        filename = f"db_backup_{timestamp}.sql"
        local_path = os.path.join(backup_base_dir, filename)

        # 2. Execute Native Dump Command
        self.stdout.write(f"Starting local database dump...")
        
        try:
            if 'postgresql' in db_engine:
                # PostgreSQL (requires PGPASSWORD env var or .pgpass file)
                os.environ['PGPASSWORD'] = db_conf['PASSWORD']
                cmd = [
                    'pg_dump',
                    '-h', db_conf['HOST'] or 'localhost',
                    '-U', db_conf['USER'],
                    '-d', db_conf['NAME'],
                    '-f', local_path
                ]
            elif 'mysql' in db_engine:
                # MySQL
                cmd = [
                    'mysqldump',
                    '-h', db_conf['HOST'] or 'localhost',
                    '-u', db_conf['USER'],
                    f"-p{db_conf['PASSWORD']}",
                    db_conf['NAME'],
                    f"--result-file={local_path}"
                ]
            elif 'sqlite3' in db_engine:
                # SQLite (Just a file copy)
                import shutil
                shutil.copy2(db_conf['NAME'], local_path)
                cmd = None
            else:
                self.stdout.write(self.style.ERROR("Unsupported Database Engine"))
                return

            if cmd:
                subprocess.run(cmd, check=True)
            
            self.stdout.write(self.style.SUCCESS(f"Local DB backup created at {local_path}"))

        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f"Database dump failed: {e}"))
            return

        # 3. OCI Upload Logic
        # 3. Check for OCI Configurations
        oci_access_key = settings.OCI['ACCESS_KEY']
        oci_secret_key = settings.OCI['SECRET_KEY']
        oci_namespace = settings.OCI['NAMESPACE']
        oci_region = settings.OCI['REGION']
        oci_bucket = settings.OCI['BUCKET_NAME']

        if all([oci_access_key, oci_secret_key, oci_namespace, oci_region, oci_bucket]):
            self.stdout.write("Uploading DB backup to OCI...")
            endpoint = f"https://{oci_namespace}.compat.objectstorage.{oci_region}.oraclecloud.com"
            
            try:
                session = boto3.Session(
                    aws_access_key_id=oci_access_key,
                    aws_secret_access_key=oci_secret_key,
                    region_name=oci_region
                )
                s3 = session.client('s3', endpoint_url=endpoint)
                s3.upload_file(local_path, oci_bucket, filename)
                self.stdout.write(self.style.SUCCESS(f"Successfully uploaded {filename} to OCI."))
            except (BotoCoreError, ClientError) as e:
                self.stdout.write(self.style.ERROR(f"OCI Upload failed: {str(e)}"))
        else:
            self.stdout.write(self.style.WARNING("OCI config missing. DB backup remains local."))