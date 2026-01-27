from django.db import models
from django.utils.text import slugify
from django.core.cache import cache
from wagtail import blocks
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from modelcluster.fields import ParentalKey
from .utilities import (
    FeatureBlock,
    RawHTMLBlock,
)
from wagtailcache.cache import WagtailCacheMixin
from home.opportunity_model import *
from home.resource_model import *



class HomePageFeaturedPost(Orderable):
    page = ParentalKey(
        "HomePage", 
        related_name="featured_posts", 
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        "cast.Post", 
        on_delete=models.CASCADE, 
        related_name="+"
    )

    panels = [
        FieldPanel("post"),
    ]


class HomePage(WagtailCacheMixin, Page):
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

    hero_description = RichTextField(
        max_length=500,
        blank=True
    )

    intro_text = RichTextField(
        max_length=1000,
        blank=True
    )

    # body = StreamField(
    #     [
    #         ("feature_block", FeatureBlock()),
    #     ],
    #     use_json_field=True,
    #     blank=True,
    # )

    @property
    def featured_post_list(self):
        cache_key = 'home_page_featured_post_list'
        data = cache.get(cache_key)
        if not data:
            data = [item.post for item in self.featured_posts.all().select_related('post')]
            cache.set(cache_key, data, 3600)

        return data
    

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_image"),
                FieldPanel("hero_text", classname="full"),
                FieldPanel("hero_description", classname="full"),
            ],
            heading="1. Hero Section Content",
        ),
        MultiFieldPanel(
            [
                FieldPanel("intro_text", classname="full"),
            ],
            heading="2. Intro Section",
        ),
        # FieldPanel("body", heading="2-4. Feature Blocks"),
        InlinePanel("featured_posts", label="Featured Posts", max_num=3),
    ]

    subpage_types = [
        "cast.Blog",
        "home.ProgramIndexPage", 
        "home.ResourcePage", 
        "home.GuidancePage",
        "home.AboutPage",
        "home.PrivacyPolicyPage",
        "home.TermsAndConditionsPage",
        "newsletter.NewsletterIndexPage",
    ]



class AboutPage(WagtailCacheMixin, Page):
    class Meta:
        verbose_name = "About"

    template = 'home/about.html'
    parent_page_types = ['home.HomePage']


    founder_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    body_text = RichTextField(
        max_length=2000,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('founder_image'),
        FieldPanel('body_text')
    ]



class PrivacyPolicyPage(WagtailCacheMixin, Page):
    class Meta:
        verbose_name = "Privacy Policy"

    template = 'home/privacy.html'
    parent_page_types = ['home.HomePage']
    
    body_text = RichTextField(
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('body_text')
    ]


class TermsAndConditionsPage(WagtailCacheMixin, Page):
    class Meta:
        verbose_name = "Terms & Conditions"

    template = 'home/privacy.html'
    parent_page_types = ['home.HomePage']
    
    body_text = RichTextField(
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('body_text')
    ]



class GuidanceSectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    nav_titile = blocks.CharBlock(required=True)
    anchor_id = blocks.CharBlock(
        required=True, 
        help_text="A unique ID for scrolling (e.g., 'subject-matter'). No spaces."
    )
    content = blocks.RichTextBlock()



class GuidancePage(WagtailCacheMixin, Page):
    class Meta:
        verbose_name = "The Essentials"

    template = 'home/essentials.html'
    parent_page_types = ['home.HomePage']

    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="The large background image for the hero section.",
    )

    hero_text = RichTextField(
        max_length=500,
        blank=True
    )

    hero_description = RichTextField(
        max_length=1000,
        blank=True
    )

    

    types_of_program = StreamField([
        ('types_of_program', GuidanceSectionBlock()),
    ], use_json_field=True, blank=True)

    mathing_program = StreamField([
        ('mathing_program', GuidanceSectionBlock()),
    ], use_json_field=True, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('hero_image'),
        FieldPanel('hero_text'),
        FieldPanel('hero_description'),
        FieldPanel('types_of_program'),
        FieldPanel('mathing_program'),
    ]


