from wagtail.admin.panels import HelpPanel
from wagtail.fields import RichTextField
from home.abstract_model import AbstractBaseFilterModel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from django.db import models
from wagtailcache.cache import WagtailCacheMixin
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from wagtail.images.models import Image 
from django.utils.html import format_html

class ResourceAcademicStage(AbstractBaseFilterModel):
    """
    e.g. books, video, podcast, films, etc.
    """
    logo = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="The provider's logo."
    )
    class Meta(AbstractBaseFilterModel.Meta):
        verbose_name = "Resource Category"
        verbose_name_plural = "Resource Categories"


class ResourceCategory(AbstractBaseFilterModel):
    logo = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="The provider's logo."
    )

    class Meta(AbstractBaseFilterModel.Meta):
        verbose_name = "Resource Type"
        verbose_name_plural = "Resource Types"


class ResourceCategories(models.Model):
    resource = ParentalKey('home.Resource', on_delete=models.CASCADE, related_name='resource_resource_types')
    program_type = models.ForeignKey('home.ResourceCategory', on_delete=models.CASCADE, related_name='+')


class ResourceAcademicStages(models.Model):
    resource = ParentalKey('home.Resource', on_delete=models.CASCADE, related_name='resource_resource_categories')
    program_type = models.ForeignKey('home.ResourceAcademicStage', on_delete=models.CASCADE, related_name='+')


class Resource(ClusterableModel):
    """
    A simple record (not a Page) managed in Wagtail.
    """
    name = models.CharField(max_length=255)
    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Resource Image"
    )
    author = models.CharField(max_length=255, blank=True)
    age_group = models.CharField(max_length=255, blank=True)
    link = models.URLField(blank=True)


    # Simplified ManyToMany (No 'through' model needed)
    categories = ParentalManyToManyField(
        'home.ResourceAcademicStage', 
        blank=True
    )
    types = ParentalManyToManyField(
        'home.ResourceCategory', 
        blank=True
    )

    panels = [
        HelpPanel(content=format_html(
            '<div style="margin-bottom: 20px;">'
            '<a href="/admin/home/resource/" class="button button-secondary">'
            '← Back to Resource List'
            '</a></div>'
        )),
        FieldPanel('name'),
        FieldPanel('author'),
        FieldPanel('image'),
        FieldPanel('age_group'),
        FieldPanel('link'),
        MultiFieldPanel([
            FieldPanel('academic_stages'),
            FieldPanel('types'),
        ], heading="Classifications")
    ]

    def __str__(self):
        return self.name

class ResourceIndexPage(WagtailCacheMixin, Page):

    template = 'home/resource_library_page.html'
    parent_page_types = ['home.HomePage']
    
    class Meta:
        verbose_name = "resource"

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

    content_panels = Page.content_panels + [
        FieldPanel('hero_image'),
        FieldPanel('hero_text'),
        FieldPanel('hero_description'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # Fetch all resources to display on the page
        context['resource_categories'] = ResourceCategory.objects.all()
        return context