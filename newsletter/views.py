from django.conf import settings
from django.http import JsonResponse
import mailchimp_marketing as MailchimpMarketing
from newsletter.models import GothamSubscriber
from django.views.decorators.http import require_POST, require_GET
from django.template.response import TemplateResponse
from logging import getLogger

logger = getLogger(__name__)

def push_to_mailchimp(email):
    if not email:
        return None
    
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": settings.MAILCHIMP_API_KEY,
        "server": settings.MAILCHIMP_SERVER
    })
    
    return client.lists.add_list_member(settings.MAILCHIMP_AUDIENCE_ID, {
        "email_address": email,
        "status": "pending", # 'pending' triggers Double Opt-in (Recommended)
    })
    


@require_POST
def newsletter_signup(request):
    email = request.POST.get('email')
    if not email:
        return JsonResponse({'status': 'error', 'message': 'Email is required.'}, status=400)

    recipient, created = GothamSubscriber.objects.update_or_create(
        email=email,
        active=1
    )
    
    try:
        res = push_to_mailchimp(email)
        return JsonResponse({'status': 'success', 'message': 'Success! Check your inbox.'})
    except Exception as e:
        logger.error(e)
        return JsonResponse({'status': 'success', 'note': 'Record updated'})
    


@require_GET
def newsletter_thankyou(request):

    return TemplateResponse(
        request,
        "thankyou.html",
    )
