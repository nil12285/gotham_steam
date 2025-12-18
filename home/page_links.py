from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.models import Page
from django.db import models

@register_setting
class WagtailPageLinks(BaseSiteSetting):
    about_page = models.ForeignKey(
        Page,
        null=True, 
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        limit_choices_to={"content_type__model": "aboutpage"}
    )

    insights_page = models.ForeignKey(
        "home.InsightsIndexPage",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )


    programs_page = models.ForeignKey(
        "home.OpportunityIndexPage",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )


    privacy_page = models.ForeignKey(
        "home.PrivacyPolicyPage",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    terms_page = models.ForeignKey(
        "home.TermsAndServicesPage",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    contact_page = models.ForeignKey(
        "home.ContactPage",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
