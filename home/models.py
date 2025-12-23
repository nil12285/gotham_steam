from django.db import models
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from .utilities import (
    FeatureBlock,
    RawHTMLBlock,
)
from wagtail.images.models import Image  # Import Wagtail Image model for explicit FK
from wagtail_color_panel.fields import ColorField
from wagtail_color_panel.blocks import NativeColorBlock
from .utilities import (
    FEATURE_LAYOUT_CHOICES,
    LINE_HEIGHT_CHOICES,
    TEXT_ALIGNMENT_CHOICES,
)
from .opportunity_model import *

class AbstractFilterModel(models.Model):
    
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)




class HomePage(Page):
    class Meta:
        verbose_name = "Gotham Homepage"
    parent_page_types = ['wagtailcore.Page']
    page_ptr = models.OneToOneField(
        Page,
        on_delete=models.CASCADE,
        parent_link=True,
        related_name='home_homepage_pointer', # Give it a unique name
    )
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    hero_text = RichTextField(
        max_length=500,
        blank=True
    )

    body = StreamField(
        [
            ("feature_block", FeatureBlock()),
        ],
        use_json_field=True,
        blank=True,
    )
    
    featured_blogs = ParentalManyToManyField(
        "cast.Post",
        blank=True,
        help_text="Select up to 3 articles to feature."
    )

    @property
    def featured_blogs_list(self):
        return self.featured_blogs.all().specific()

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_image"),
                FieldPanel("hero_text", classname="full"),
            ],
            heading="1. Hero Section Content",
        ),
        FieldPanel("body", heading="2-4. Feature Blocks"),
        MultiFieldPanel(
            [
                FieldPanel("featured_blogs"),
            ],
            heading="5. Featured Insights & Resources",
        ),
    ]

    subpage_types = [
        "home.ProgramIndexPage", 
        "cast.Blog",
        "home.ContactPage",
        "home.PrivacyPolicyPage",
        "home.TermsAndServicesPage",
        "newsletter.NewsletterIndexPage"
    ]


    


class ContactPage(Page):
    parent_page_types = ['home.HomePage']
    intro = models.TextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("intro", classname="full"),
    ]


class PrivacyPolicyPage(Page):
    parent_page_types = ['home.HomePage']
    body = StreamField(
        [
            ("paragraph", blocks.RichTextBlock()),
            ("raw_html", RawHTMLBlock()),
        ],
        use_json_field=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


class TermsAndServicesPage(Page):
    parent_page_types = ['home.HomePage']
    body = StreamField(
        [
            ("paragraph", blocks.RichTextBlock()),
            ("raw_html", RawHTMLBlock()),
        ],
        use_json_field=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

