from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail_newsletter.models import NewsletterPageMixin
from wagtail_newsletter.models import NewsletterRecipients
from django.http import Http404
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from django.utils.translation import gettext_lazy as _
from datetime import datetime

class HeadingBlock(blocks.CharBlock):
    class Meta:
        template = "newsletter/blocks/heading.html"


class RichParagraphBlock(blocks.RichTextBlock):
    class Meta:
        template = "newsletter/blocks/paragraph.html"



class NewsletterIndexPage(Page):
    intro = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = ["newsletter.NewsletterPage"]


class NewsletterPage(NewsletterPageMixin, Page):
    
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField(
        [
            ("heading", HeadingBlock()),
            ("paragraph", RichParagraphBlock()),
            ("image", ImageChooserBlock()),
            ("button", blocks.StructBlock([
                ("text", blocks.CharBlock()),
                ("url", blocks.URLBlock()),
            ])),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("hero_image"),
        FieldPanel("body"),
    ]

    # THIS is what wagtail-newsletter renders
    newsletter_template = "newsletter/newsletter_page.html"

    parent_page_types = ["newsletter.NewsletterIndexPage"]
    subpage_types = []

    def serve(self, request):
        if not request.user.is_authenticated:
            raise Http404()
        return super().serve(request)

    def get_newsletter_context(self):
        context = super().get_newsletter_context()
        # Manually providing base_url to the template
        context['base_url'] = self.get_site().root_url
        return context





class GothamNewsletterRecipient(NewsletterRecipients):
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=False)
    created = CreationDateTimeField(_('created'))
    modified = ModificationDateTimeField(_('modified'), auto_now=True)

    def save(self, **kwargs):
        if not self.pk:
            self.created = datetime.now()

        self.update_modified = kwargs.pop('update_modified', getattr(self, 'update_modified', True))
        super().save(**kwargs)

    class Meta:
        get_latest_by = 'modified'
        verbose_name = "Subscriber"