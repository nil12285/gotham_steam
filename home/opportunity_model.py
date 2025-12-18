from django.db import models
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, FieldRowPanel
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
from collections import OrderedDict

YES_NO_CHOICES = [
    ("Yes", "Yes"),
    ("No", "No"),
    ("Varies", "Varies/N/A"),
]


class AbstractBaseFilterModel(models.Model):
    """
    Base model for all dynamic filter choices like ProgramType, Location, etc.
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, max_length=255, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['name']



class ProgramType(AbstractBaseFilterModel):
    class Meta(AbstractBaseFilterModel.Meta):
        verbose_name = "Program Type"
        verbose_name_plural = "Program Types"

class ProgramDelivery(AbstractBaseFilterModel):
    class Meta(AbstractBaseFilterModel.Meta):
        verbose_name = "Program Delivery Method"
        verbose_name_plural = "Program Delivery Methods"

class ProgramLocation(AbstractBaseFilterModel):
    class Meta(AbstractBaseFilterModel.Meta):
        verbose_name = "Location Type"
        verbose_name_plural = "Location Types"

class NYCNeighborhood(AbstractBaseFilterModel):
    class Meta(AbstractBaseFilterModel.Meta):
        verbose_name = "NYC Neighborhood"
        verbose_name_plural = "NYC Neighborhoods"

class SessionStart(AbstractBaseFilterModel):
    class Meta(AbstractBaseFilterModel.Meta):
        verbose_name = "Session Start Month"
        verbose_name_plural = "Session Start Months"

class SessionLength(AbstractBaseFilterModel):
    class Meta(AbstractBaseFilterModel.Meta):
        verbose_name = "Session Length"
        verbose_name_plural = "Session Lengths"

class FeesCategory(AbstractBaseFilterModel):
    class Meta(AbstractBaseFilterModel.Meta):
        verbose_name = "Fees Category"
        verbose_name_plural = "Fees Categories"

class GenderFilter(AbstractBaseFilterModel):
    class Meta(AbstractBaseFilterModel.Meta):
        verbose_name = "Gender Filter"
        verbose_name_plural = "Gender Filters"


class Selectivity(AbstractBaseFilterModel):
    class Meta(AbstractBaseFilterModel.Meta):
        verbose_name = "Program Selectivity"
        verbose_name_plural = "Program Selectivity"


# New Dynamic Filter Models based on JSON fields:

class FocusTopic(AbstractBaseFilterModel):
    class Meta(AbstractBaseFilterModel.Meta):
        verbose_name = "Focus/Topic"
        verbose_name_plural = "Focus/Topics"

class AgeGroup(AbstractBaseFilterModel):
    class Meta(AbstractBaseFilterModel.Meta):
        verbose_name = "Age Group"
        verbose_name_plural = "Age Groups"



class ProgramTag(TaggedItemBase):
    content_object = ParentalKey(
        'home.Program',
        on_delete=models.CASCADE,
        related_name='tagged_items'
    )

class ProgramProgramType(models.Model):
    page = ParentalKey('home.Program', on_delete=models.CASCADE, related_name='program_program_types')
    program_type = models.ForeignKey('home.ProgramType', on_delete=models.CASCADE, related_name='+')

class ProgramProgramDelivery(models.Model):
    page = ParentalKey('home.Program', on_delete=models.CASCADE, related_name='program_delivery_methods')
    delivery_method = models.ForeignKey('home.ProgramDelivery', on_delete=models.CASCADE, related_name='+')

class ProgramProgramLocation(models.Model):
    page = ParentalKey('home.Program', on_delete=models.CASCADE, related_name='program_locations')
    location = models.ForeignKey('home.ProgramLocation', on_delete=models.CASCADE, related_name='+')

class ProgramNYCNeighborhood(models.Model):
    page = ParentalKey('home.Program', on_delete=models.CASCADE, related_name='program_neighborhoods')
    neighborhood = models.ForeignKey('home.NYCNeighborhood', on_delete=models.CASCADE, related_name='+')

class ProgramSessionStart(models.Model):
    page = ParentalKey('home.Program', on_delete=models.CASCADE, related_name='program_session_starts')
    session_start = models.ForeignKey('home.SessionStart', on_delete=models.CASCADE, related_name='+')

class ProgramSessionLength(models.Model):
    page = ParentalKey('home.Program', on_delete=models.CASCADE, related_name='program_session_lengths')
    session_length = models.ForeignKey('home.SessionLength', on_delete=models.CASCADE, related_name='+')

class ProgramFeesCategory(models.Model):
    page = ParentalKey('home.Program', on_delete=models.CASCADE, related_name='program_fees_categories')
    fees_category = models.ForeignKey('home.FeesCategory', on_delete=models.CASCADE, related_name='+')

class ProgramGenderFilter(models.Model):
    page = ParentalKey('home.Program', on_delete=models.CASCADE, related_name='program_gender_filters')
    gender_filter = models.ForeignKey('home.GenderFilter', on_delete=models.CASCADE, related_name='+')

class ProgramFocusTopic(models.Model):
    page = ParentalKey('home.Program', on_delete=models.CASCADE, related_name='program_focus_topics')
    focus_topic = models.ForeignKey('home.FocusTopic', on_delete=models.CASCADE, related_name='+')

class ProgramAgeGroup(models.Model):
    page = ParentalKey('home.Program', on_delete=models.CASCADE, related_name='program_age_groups')
    age_group = models.ForeignKey('home.AgeGroup', on_delete=models.CASCADE, related_name='+')


class Program(Page):
    """
    Model for an individual STEM program entry.
    """
    template = 'home/program_page.html'
    class Meta:
        verbose_name = "program"

    parent_page_types = ['home.ProgramIndexPage']
    subpage_types = []

    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, default='USA')
    # --- Provider & Vetting Details ---
    logo_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="The provider's logo."
    )

    accreditation = models.CharField(max_length=255, null=True, blank=True, help_text="Accrediting body name.")
    
    age_groups = ParentalManyToManyField(
        AgeGroup,
        through='home.ProgramAgeGroup',
        blank=True,
        help_text="The age/school-level groups targeted (e.g., Middle School, High School)."
    )
    application_deadline = models.DateField(null=True, blank=True, help_text="Last day to apply.")
    application_details = models.CharField(max_length=255, null=True, blank=True)
    application_selective = models.CharField(
        max_length=10,
        choices=YES_NO_CHOICES,
        default="Varies",
        null=True,
        blank=True,
        help_text="Is the application process highly selective?"
    )
    attached_files = models.CharField(max_length=255, null=True, blank=True)  
    
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    contact_private_email = models.EmailField(max_length=255, null=True, blank=True)
    contact_private_phone = models.CharField(max_length=255, null=True, blank=True)
    cost = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    
    # --- Dates, Deadlines & Scheduling ---
    application_deadline = models.DateField(null=True, blank=True, help_text="application_deadline_date")
    event_start_date = models.DateField(null=True, blank=True, help_text="For single-event programs, the start date.")
    event_end_date = models.DateField(null=True, blank=True, help_text="For single-event programs, the end date.")

    last_updated = models.DateField(null=True, blank=True)
    is_exceptional = models.BooleanField(default=False, help_text="exceptional_experience")
    
    facebook = models.URLField(max_length=255, null=True, blank=True)
    twitter = models.URLField(max_length=255, null=True, blank=True)
    instagram = models.URLField(max_length=255, null=True, blank=True)
    youtube = models.URLField(max_length=255, null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    press_links = models.CharField(max_length=255, null=True, blank=True)

    program_types = ParentalManyToManyField(
        ProgramType,
        through='home.ProgramProgramType',
        blank=True,
        help_text="The general categories this program falls under (e.g., Class, Summer Day Camp)."
    )

    locations = ParentalManyToManyField(
        ProgramLocation,
        through='home.ProgramProgramLocation',
        blank=True,
        help_text="The geographical area of operation (e.g., NYC, Nationwide)."
    )
    
    gender = ParentalManyToManyField(
        GenderFilter,
        through='home.ProgramGenderFilter',
        blank=True,
        help_text="Who the program is for (e.g., Coed, Girls Only)."
    )
    
    focus_topics = ParentalManyToManyField(
        FocusTopic,
        through='home.ProgramFocusTopic',
        blank=True,
        help_text="The STEM topics covered (e.g., Mathematics, Engineering)."
    )

    my_notes = models.CharField(max_length=255, null=True, blank=True)
    logo_path = models.CharField(max_length=255, null=True, blank=True)

    nyc_neighborhood = ParentalManyToManyField(
        NYCNeighborhood,
        through='home.ProgramNYCNeighborhood',
        blank=True,
        help_text="Specific NYC neighborhoods where the program takes place."
    )

    program_overview = RichTextField(
        blank=True,
        null=True,
        help_text="Detailed description and program overview.",
        features=RICH_TEXT_BLOCK_FEATURES
    )
    
    program_delivery = ParentalManyToManyField(
        ProgramDelivery,
        through='home.ProgramProgramDelivery',
        blank=True,
        help_text="How the program is delivered (e.g., In-person, Online, Hybrid)."
    )

    session_start = ParentalManyToManyField(
        SessionStart,
        through='home.ProgramSessionStart',
        blank=True
    )

    fees_category = ParentalManyToManyField(
        FeesCategory,
        through='home.ProgramFeesCategory',
        blank=True,
        help_text="free_low_cost_program"
    )

    session_length = ParentalManyToManyField(
        SessionLength,
        through='home.ProgramSessionLength',
        blank=True
    )
    
    program_summary = models.TextField(null=True, blank=True)
    referred_by = models.CharField(max_length=255, null=True, blank=True)
    
    provider  = models.CharField(max_length=255, null=True, blank=True)
    scholarship_fin_aid  = models.CharField(max_length=255, null=True, blank=True)
    scholarship_fin_aid_details  = models.CharField(max_length=255, null=True, blank=True)
    years_in_business  = models.CharField(max_length=255, null=True, blank=True)
    
    staff_details = models.TextField(null=True, blank=True, help_text="Brief details about the staff/founders.")
    scholarship_details = models.TextField(null=True, blank=True, help_text="Details about scholarship or financial aid.")
    

    # --- Content Panels ---
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('logo_image'),
                FieldPanel('program_summary', help_text="Appears on the search results page."),
                FieldPanel('program_overview', classname="full"),
                FieldRowPanel([
                    FieldPanel('staff_details'),
                    FieldPanel('is_exceptional'),
                ], heading="Staff & Program Flag"),
                FieldPanel('scholarship_details'),
            ],
            heading="1. Program Content & Overview"
        ),

        MultiFieldPanel(
            [
                FieldRowPanel([
                    FieldPanel('age_groups'),
                    FieldPanel('focus_topics'),    
                ]),
                FieldRowPanel([
                    FieldPanel('program_types'),
                    FieldPanel('program_delivery'),
                ]),
                FieldPanel('gender'),
            ],
            heading="2. Core Program Filters",
        ),

        MultiFieldPanel(
            [
                FieldRowPanel([
                    FieldPanel('locations'),
                    FieldPanel('nyc_neighborhood'),
                ], heading="Location Details"),
                FieldRowPanel([
                    FieldPanel('session_start'),
                    FieldPanel('session_length'),
                ], heading="Schedule Details"),
            ],
            heading="3. Location & Schedule Filters"
        ),

        MultiFieldPanel(
            [
                FieldRowPanel([
                    FieldPanel('cost'),
                    FieldPanel('fees_category'),
                ], heading="Program Cost"),
                FieldRowPanel([
                    FieldPanel('application_deadline'),
                    FieldPanel('application_selective'),
                ], heading="Application"),
                FieldRowPanel([
                    FieldPanel('event_start_date'),
                    FieldPanel('event_end_date'),
                ], heading="Event Dates"),
                FieldPanel('scholarship_fin_aid'),
                FieldPanel('scholarship_fin_aid_details'),
            ],
            heading="4. Financial & Time Details"
        ),

        # --- INTERNAL / VETTING TAB (Grouping fields not used on the detail page) ---
        MultiFieldPanel(
            [
                FieldRowPanel([
                    FieldPanel('provider'),
                    
                ], heading="Organization Details"),

                FieldPanel('accreditation'),
                FieldPanel('years_in_business'),
                MultiFieldPanel([
                    FieldPanel('name'),
                    FieldPanel('email'),
                    FieldPanel('phone'),
                    FieldPanel('address'),
                    FieldRowPanel([
                        FieldPanel('city'),
                        FieldPanel('state'),
                        FieldPanel('zip_code'),
                        FieldPanel('country'),
                    ], heading="Location Address"),
                ], heading="Provider Contact & Location"),
                
                MultiFieldPanel([
                    FieldPanel('contact_person'),
                    FieldPanel('contact_private_email'),
                    FieldPanel('contact_private_phone'),
                ], heading="Internal Contact Info"),
                
                MultiFieldPanel([
                    FieldPanel('website'),
                    FieldPanel('facebook'),
                    FieldPanel('twitter'),
                    FieldPanel('instagram'),
                    FieldPanel('youtube'),
                    FieldPanel('press_links'),
                ], heading="Social & Website Links"),
                
                MultiFieldPanel([
                    FieldPanel('application_details'),
                    FieldPanel('attached_files'),
                    FieldPanel('referred_by'),
                    FieldPanel('last_updated'),
                    FieldPanel('logo_path', help_text="Legacy/Internal Path"),
                    FieldPanel('my_notes', classname="full"),
                ], heading="Vetting & Notes"),
            ],
            heading="5. Internal Vetting & Admin Details (Not Public)",
            classname="collapsed" # Optionally collapse this internal section by default
        ),
    ]


    # Override get_context to fetch all live opportunities for initial load (optional)
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # helper to join M2M names
        def get_m2m_names(manager):
            return ", ".join([obj.name for obj in manager.all()]) if manager.exists() else "Varies/N/A"

        # Mapping mockup labels to model fields
        essential_info = OrderedDict([
            ("Program type", {
                "value": get_m2m_names(self.program_types),
                "field": "program_types"
            }),
            ("Program delivery", {
                "value": get_m2m_names(self.program_delivery),
                "field": "program_delivery"
            }),
            ("Location", {
                "value": get_m2m_names(self.locations),
                "field": "locations"
            }),
            ("NYC Neighborhood", {
                "value": get_m2m_names(self.nyc_neighborhood),
                "field": "nyc_neighborhood"
            }),
            ("Topics", {
                "value": get_m2m_names(self.focus_topics),
                "field": "focus_topics"
            }),
            ("Session Starts", {
                "value": get_m2m_names(self.session_start),
                "field": "session_start"
            }),
            ("Session length", {
                "value": get_m2m_names(self.session_length),
                "field": "session_length"
            }),
            ("Ages", {
                "value": get_m2m_names(self.age_groups),
                "field": "age_groups"
            }),
            ("Gender", {
                "value": get_m2m_names(self.gender),
                "field": "gender"
            }),
            ("Selective", {
                "value": self.get_application_selective_display() if self.application_selective else "Varies",
                "field": "application_selective"
            }),
            ("Application Deadline", {
                "value": self.application_deadline.strftime("%B %d, %Y") if self.application_deadline else "Rolling/N/A",
                "field": "application_deadline"
            }),
            ("Cost", {
                "value": self.cost if self.cost else "Varies/N/A",
                "field": "cost"
            }),
            ("Scholarships/Financial Aid", {
                "value": self.scholarship_fin_aid if self.scholarship_fin_aid else "Contact for details",
                "field": "scholarship_fin_aid"
            }),
            ("Accreditation", {
                "value": self.accreditation if self.accreditation else "N/A",
                "field": "accreditation"
            }),
            ("Years in Business", {
                "value": self.years_in_business if self.years_in_business else "N/A",
                "field": "years_in_business"
            }),
        ])

        context['essential_info'] = essential_info
        return context



class ProgramIntroBlock(blocks.StructBlock):
    """
    A block for alternating image/text feature sections used on the HomePage.
    Updated to use ChoiceBlock for better user experience with Bootstrap utilities.
    """

    text_left = blocks.RichTextBlock(
        required=True,
        features=RICH_TEXT_BLOCK_FEATURES,
        help_text="Text content displayed next to the image. Supports standard formatting and color via the 'colour' feature.",
    )

    # Standard Wagtail rich text editor for formatted body content
    text_right = blocks.RichTextBlock(
        required=True,
        features=RICH_TEXT_BLOCK_FEATURES,
        help_text="Text content displayed next to the image. Supports standard formatting and color via the 'colour' feature.",
    )

    background_color = NativeColorBlock(default="#C9BDEC")
    text_color = NativeColorBlock(default="#000000")

    # Replaced CharField with ChoiceBlock for user-friendly line height selection
    line_height_class = blocks.ChoiceBlock(
        choices=LINE_HEIGHT_CHOICES,
        default="",
        required=False,
        help_text="Select the line spacing for the text in this block.",
    )

    # Alignment remains a restricted choice for UI consistency
    text_alignment = blocks.ChoiceBlock(
        choices=TEXT_ALIGNMENT_CHOICES,
        default="start",
        required=True,
        help_text="Choose the alignment of the text content (Left/Right/Center).",
    )

    class Meta:
        icon = "grip"
        template = "home/blocks/intro_block.html"



class ProgramIndexPage(Page):
    
    class Meta:
        verbose_name = "programs"
    
    template = 'home/program_search_results.html'
    
    subpage_types = ['home.Program']
    parent_page_types = ['home.HomePage']

    PROGRAM_FILTERS = OrderedDict({
         'program_types' : {
            'title' : 'type of program',
            'field' : 'program_types__slug',
            'data' : ProgramType.objects.all().order_by('name'),
            'multiselect' : True
        },
        'program_delivery' : {
            'title' : 'program delivery',
            'field' : 'program_delivery__slug',
            'data' : ProgramDelivery.objects.all().order_by('name'),
            'multiselect' : True
        },
        'focus_topics' : {
            'title' : 'topics',
            'field' : 'focus_topics__slug',
            'data' : FocusTopic.objects.all().order_by('name'),
            'multiselect' : True
        },
        'locations' : {
            'title' : 'location',
            'field' : 'locations__slug',
            'data' : ProgramLocation.objects.all().order_by('name'),
            'multiselect' : True
        },
        'nyc_neighborhood' : {
            'title' : 'nyc neighborhood',
            'field' : 'nyc_neighborhood__slug',
            'data' : NYCNeighborhood.objects.all().order_by('name'),
            'multiselect' : True
        },
        'session_start' : {
            'title' : 'session start',
            'field' : 'session_start__slug',
            'data' : SessionStart.objects.all().order_by('name'),
            'multiselect' : True
        },
        'session_length' : {
            'title' : 'session length',
            'field' : 'session_length__slug',
            'data' : SessionLength.objects.all().order_by('name'),
            'multiselect' : True
        },
        'age_groups' : {
            'title' : 'ages',
            'field' : 'age_groups__slug',
            'data' : AgeGroup.objects.all().order_by('name'),
            'multiselect' : True
        },
        'gender' : {
            'title' : 'gender',
            'field' : 'gender__slug',
            'data' : GenderFilter.objects.all().order_by('name'),
            'multiselect' : True
        },
        'fees_category' : {
            'title' : 'fees',
            'field' : 'fees_category__slug',
            'data' : FeesCategory.objects.all().order_by('name'),
            'multiselect' : True
        },
        'selectivity' : {
            'title' : 'selective',
            'field' : 'selectivity__slug',
            'data' : Selectivity.objects.all().order_by('name'),
            'multiselect' : True
        },
    })
    
    
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="The large background image for the hero section.",
    )

    intro = StreamField(
        [
            ("intro_block", ProgramIntroBlock()),
            ("raw_html", RawHTMLBlock()),
        ],
        block_counts={
            "intro_block": {"min_num": 1}
        },
        null=True,
        blank=True,
        use_json_field=True,
        help_text="Add alternating feature blocks (image and text) or raw HTML for the main body of the homepage.",
    )

    
    content_panels = Page.content_panels + [
        FieldPanel('hero_image'),
        FieldPanel('intro'),
    ]


    def serve(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.template = "home/blocks/programs_results.html"
        else:
            self.template = "home/program_search_results.html"
            
        return super().serve(request, *args, **kwargs)
    
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        opportunities = Program.objects.descendant_of(self).live()
        search_query = request.GET.get('q', '').strip()
        get_params = request.GET
        selected_filters = {}

        if search_query:
            opportunities = opportunities.search(search_query)
        
        for param_name, config in self.PROGRAM_FILTERS.items():
            param_values = get_params.getlist(param_name) 
            
            if param_values:
                param_values = [v for v in param_values if v]
                if not param_values:
                    continue

                selected_filters[param_name] = param_values
                if search_query and hasattr(opportunities, 'get_queryset'):
                    program_ids = [obj.pk for obj in opportunities]
                    opportunities = Program.objects.filter(pk__in=program_ids)
                elif search_query: 
                    program_ids = [obj.pk for obj in opportunities]
                    opportunities = Program.objects.filter(pk__in=program_ids)

                field_path = config['field']

                if config.get('multiselect', False):
                    filter_key = f"{field_path}__in"
                    opportunities = opportunities.filter(**{filter_key: param_values}).distinct()
                else:
                    filter_key = field_path
                    opportunities = opportunities.filter(**{filter_key: param_values[0]})
        
        page_num = get_params.get('page', 1)
        paginator = Paginator(opportunities, 10) 

        try:
            paginated_opportunities = paginator.page(page_num)
        except PageNotAnInteger:
            
            paginated_opportunities = paginator.page(1)
        except EmptyPage:
            paginated_opportunities = paginator.page(paginator.num_pages)
            
        if search_query:
            selected_filters['q'] = search_query
            
        context.update({
            'search_query': search_query,
            'opportunities': paginated_opportunities, 
            'program_filters' : self.PROGRAM_FILTERS,
            'selected_filters': selected_filters, 
            'form_action_url': self.url,
        })
            
        return context