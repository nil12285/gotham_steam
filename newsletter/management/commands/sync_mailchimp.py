from django.core.management.base import BaseCommand
from django.conf import settings
import mailchimp_marketing as MailchimpMarketing
from newsletter.models import GothamSubscriber

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
            for status in [('unsubscribed',False),('pending',False)]:
                response = client.lists.get_list_members_info(
                    settings.MAILCHIMP_AUDIENCE_ID, 
                    status=status[0],
                    count=1000  # Adjust based on list size
                )
                self.stdout.write(f"Found {len(response['members'])} users with {status[0]} status.",self.style.NOTICE)
                for member in response['members']:
                    email = member['email_address']
                    # Mark as inactive in your local DB
                    updated = GothamSubscriber.objects.filter(
                        email=email
                    ).update(active=status[1])

                    if updated:
                        self.stdout.write(f"Synced unsubscribe for: {email}")
                
        except Exception as e:
            self.stdout.write(f"Error: {e}")

