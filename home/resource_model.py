from wagtail.admin.panels import HelpPanel
from home.abstract_model import AbstractBaseFilterModel
from modelcluster.fields import ParentalKey, ParentalManyToManyField, ForeignKey
from modelcluster.models import ClusterableModel
from django.db import models
from wagtailcache.cache import WagtailCacheMixin
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from wagtail.images.models import Image 
from django.utils.html import format_html

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
        verbose_name = "Resource Category"
        verbose_name_plural = "Resource Categories"


class ResourceType(AbstractBaseFilterModel):
    class Meta(AbstractBaseFilterModel.Meta):
        verbose_name = "Resource Type"
        verbose_name_plural = "Resource Types"


class ResourceTypes(models.Model):
    resource = ParentalKey('home.Resource', on_delete=models.CASCADE, related_name='resource_resource_types')
    program_type = models.ForeignKey('home.ResourceType', on_delete=models.CASCADE, related_name='+')


class ResourceCategories(models.Model):
    resource = ParentalKey('home.Resource', on_delete=models.CASCADE, related_name='resource_resource_categories')
    program_type = models.ForeignKey('home.ResourceCategory', on_delete=models.CASCADE, related_name='+')


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
        'home.ResourceCategory', 
        blank=True
    )
    types = ParentalManyToManyField(
        'home.ResourceType', 
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
            FieldPanel('categories'),
            FieldPanel('types'),
        ], heading="Classifications")
    ]

    def __str__(self):
        return self.name
    
    

class ResourcePage(WagtailCacheMixin, Page):

    template = 'home/resource_page.html'
    parent_page_types = ['home.HomePage']

    class Meta:
        verbose_name = "resource"


    def get_context(self, request):
        context = super().get_context(request)
        # Fetch all resources to display on the page
        context['resources'] = Resource.objects.all()
        return context