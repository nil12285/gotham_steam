from django.core.management.base import BaseCommand
from django.conf import settings
import mailchimp_marketing as MailchimpMarketing
from newsletter.models import GothamNewsletterRecipient

class Command(BaseCommand):
    help = 'Syncs unsubscribes from Mailchimp to local DB'

    def handle(self, *args, **options):
        client = MailchimpMarketing.Client()
        client.set_config({
            "api_key": settings.MAILCHIMP_API_KEY,
            "server": settings.MAILCHIMP_SERVER
        })

        # Fetch only unsubscribed members
        try:
            response = client.lists.get_list_members_info(
                settings.MAILCHIMP_AUDIENCE_ID, 
                status="unsubscribed",
                count=1000  # Adjust based on list size
            )
            
            for member in response['members']:
                email = member['email_address']
                # Mark as inactive in your local DB
                updated = GothamNewsletterRecipient.objects.filter(
                    email=email, 
                    is_active=True
                ).update(is_active=False)
                if updated:
                    self.stdout.write(f"Synced unsubscribe for: {email}")

        except Exception as e:
            self.stdout.write(f"Error: {e}")

