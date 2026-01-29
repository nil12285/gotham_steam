from wagtail.admin.panels import HelpPanel
from wagtail.fields import RichTextField
from home.abstract_model import AbstractBaseFilterModel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
        verbose_name = "Resource Academic Stage"
        verbose_name_plural = "Resource Academic Stages"


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
        blank=True,
        related_name='resource_categories'
    )
    types = ParentalManyToManyField(
        'home.ResourceCategory', 
        blank=True,
        related_name='resources'
    )
    academic_stages = ParentalManyToManyField(
        'home.ResourceAcademicStage', 
        blank=True,
        related_name='resource_academic_stages'
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
    

class ResourceSearchResultPage(WagtailCacheMixin, Page):

    template = 'home/resource_search_results.html'
    parent_page_types = ['home.HomePage']
    
    class Meta:
        verbose_name = "resource search results"

    RESOURCE_FILTERS = {
        'cat': {
            'field': 'types',
            'multiselect': True,
        },
        'stage': {
            'field': 'academic_stages',
            'multiselect': True,
        },
    }


    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        all_resources = Resource.objects.all().prefetch_related('types', 'academic_stages')
        get_params = request.GET
        selected_filters = {}

        for param_name, config in self.RESOURCE_FILTERS.items():
            param_values = [v for v in get_params.getlist(param_name) if v]
            if param_values:
                selected_filters[param_name] = param_values

        filtered_resources = all_resources
        for param_name, values in selected_filters.items():
            config = self.RESOURCE_FILTERS[param_name]
            field_path = config['field']
            if config.get('multiselect', False):
                filtered_resources = filtered_resources.filter(**{f"{field_path}__slug__in": values}).distinct()
            else:
                filtered_resources = filtered_resources.filter(**{f"{field_path}__slug": values[0]})

        
        cat_filter_resources = all_resources
        if 'stage' in selected_filters:
            cat_filter_resources = cat_filter_resources.filter(academic_stages__slug__in=selected_filters['stage']).distinct()

        stage_filter_resources = all_resources
        if 'cat' in selected_filters:
            stage_filter_resources = stage_filter_resources.filter(types__slug=selected_filters['cat'][0]).distinct()

        categories = ResourceCategory.objects.annotate(
            resource_count=models.Count(
                'resources', 
                filter=models.Q(resources__in=cat_filter_resources)
            )
        )

        academic_stages = ResourceAcademicStage.objects.annotate(
            resource_count=models.Count(
                'resource_academic_stages', 
                filter=models.Q(resource_academic_stages__in=stage_filter_resources)
            )
        )

        page_num = get_params.get('page', 1)
        paginator = Paginator(filtered_resources, 10) 
        
        try:
            paginated_resources = paginator.page(page_num)
        except (PageNotAnInteger, EmptyPage):
            paginated_resources = paginator.page(1)

        context.update({
            'resources': paginated_resources, 
            'selected_filters': selected_filters,
            'categories': categories,
            'academic_stages': academic_stages,
        })
        return context