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
from wagtail_newsletter.models import NewsletterPageMixin
from .utilities import (
    FeatureBlock,
    RawHTMLBlock,
    RICH_TEXT_BLOCK_FEATURES,
)
from wagtail.images.models import Image  # Import Wagtail Image model for explicit FK
from wagtail_color_panel.fields import ColorField
from wagtail_color_panel.blocks import NativeColorBlock
from wagtail_newsletter.models import NewsletterPageMixin
from .utilities import (
    RICH_TEXT_BLOCK_FEATURES,
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



class InsightsArticlePage(Page):
    
    subpage_types = []
    parent_page_types = ['home.InsightsIndexPage']

    date = models.DateField("Post date")
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    body = StreamField(
        [
            ("paragraph", blocks.RichTextBlock(features=RICH_TEXT_BLOCK_FEATURES)),
            ("image", ImageChooserBlock()),
            ("heading", blocks.CharBlock(classname="full title", icon="title")),
            ("quote", blocks.BlockQuoteBlock()),
            ("raw_html", RawHTMLBlock()),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('search_description'),
        FieldPanel('date'),
        FieldPanel('main_image'),
        FieldPanel('body'),
    ]
    
    



class InsightsIndexPage(Page):
    
    class Meta:
        verbose_name = "Insights"

    parent_page_types = ['home.HomePage']
    subpage_types = [
        "cast.Blog",
    ]
    
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["articles"] = self.get_children().live().order_by("-first_published_at")
        return context


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
        "home.InsightsArticlePage",
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
        "home.InsightsIndexPage",
        "home.ContactPage",
        "home.PrivacyPolicyPage",
        "home.TermsAndServicesPage",
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
            ("paragraph", blocks.RichTextBlock(features=RICH_TEXT_BLOCK_FEATURES)),
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
            ("paragraph", blocks.RichTextBlock(features=RICH_TEXT_BLOCK_FEATURES)),
            ("raw_html", RawHTMLBlock()),
        ],
        use_json_field=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


