from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.shortcuts import render
from django.conf import settings
from home.opportunity_model import ProgramIndexPage
import requests
import logging

# Set up logging
logger = logging.getLogger(__name__)


def send_mail(subject, message, from_email, recipient_list, fail_silently=True):
    return True


class ContactUs(TemplateView):
    template_name = 'home/contact_us.html'
    
    def get(self, request, *args, **kwargs):

        context_data = self.get_context_data(request=request)
        context_data['mode'] = 'default'
        context_data['RECAPTCHA_SITE_KEY'] = settings.RECAPTCHA_SITE_KEY

        mode = self.kwargs.get('mode')
        if mode:
            mode = mode.strip().lower()
            context_data['mode'] = mode
            
        return self.render_to_response(context_data)
    

    def post(self, request, *args, **kwargs):

        context_data = self.get_context_data(request=request)
        context_data['mode'] = 'default'
        context_data['RECAPTCHA_SITE_KEY'] = settings.RECAPTCHA_SITE_KEY
        mode = self.kwargs.get('mode')
        if mode:
            mode = mode.strip().lower()
            context_data['mode'] = mode

        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            "event": {
                "token": recaptcha_response,
                "expectedAction": "contact-us",
                "siteKey": settings.RECAPTCHA_SITE_KEY,
            }
        }
        
        r = requests.post(
            url=f'https://recaptchaenterprise.googleapis.com/v1/projects/{settings.GOOGLE_PROJECT_ID}/assessments?key={settings.GOOGLE_API_KEY}',
            json=data
        )
        result = r.json()
        score = result.get('riskAnalysis', {}).get('score', 0)
        is_valid = result.get('tokenProperties', {}).get('valid', False)

        if is_valid and score >= 0.7:
            pass
        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return self.render_to_response(context_data)
            
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', 'N/A')
        subject = request.POST.get('subject', 'N/A')
        program_name = request.POST.get('program_name', 'N/A')
        experience = request.POST.get('experience', 'N/A')
        message = request.POST.get('message')
        mode = self.kwargs.get('mode', 'general')

        email_body = f"""
        New Contact Form Submission ({mode.upper()})
        -------------------------------------------
        Name: {name}
        Email: {email}
        Phone: {phone}
        Subject : {subject}
        Program: {program_name}
        Experience: {experience}
        
        Comments/Message:
        {message}
        """
        # 3. Send Email via AWS SES
        try:
            send_mail(
                subject=f"Contact Form ({mode}): {name}",
                message=email_body,
                from_email="verified-sender@yourdomain.com", # Must be verified in AWS SES
                recipient_list=["info@stellark.com"],
                fail_silently=False,
            )
            messages.success(
                request, 
                message= """
                Thank you for reaching out! Your message has been successfully received.
                A member of our team will review your inquiry and get back to you within 24 hours.
                """
            )
            target = ProgramIndexPage.objects.live().first()
            if target:
                return redirect(target.get_url(request))

        except Exception as e:
            messages.error(request, e)
            logger.error(e)
    
        return self.render_to_response(context_data)