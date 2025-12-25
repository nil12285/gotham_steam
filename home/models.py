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
            ],
            heading="1. Hero Section Content",
        ),
        FieldPanel("body", heading="2-4. Feature Blocks"),
        InlinePanel("featured_posts", label="Featured Posts", max_num=3),
    ]

    subpage_types = [
        "home.ProgramIndexPage", 
        "cast.Blog",
        "home.GuidancePage",
        "home.AboutPage",
        "home.PrivacyPolicyPage",
        "home.TermsAndServicesPage",
        "newsletter.NewsletterIndexPage",
    ]



class AboutPage(Page):
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

    


class GuidanceSectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    nav_titile = blocks.CharBlock(required=True)
    anchor_id = blocks.CharBlock(
        required=True, 
        help_text="A unique ID for scrolling (e.g., 'subject-matter'). No spaces."
    )
    content = blocks.RichTextBlock()



class GuidancePage(Page):
    class Meta:
        verbose_name = "Guidance"

    template = 'home/guidance.html'
    parent_page_types = ['home.HomePage']

    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="The large background image for the hero section.",
    )

    intro_title = RichTextField(
        max_length=500,
        blank=True
    )

    intro_text = RichTextField(
        max_length=500,
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
        FieldPanel('intro_title'),
        FieldPanel('intro_text'),
        FieldPanel('types_of_program'),
        FieldPanel('mathing_program'),
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

