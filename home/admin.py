from wagtail_modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from home.models import (
    Program,
    ProgramType,
    ProgramDelivery,
    ProgramLocation,
    NYCNeighborhood,
    SessionStart,
    SessionLength,
    FeesCategory,
    GenderFilter,
    FocusTopic,
    AgeGroup, 
    Resource,
    ResourceCategory,
    ResourceAcademicStage
)

class ProgramTypeAdmin(ModelAdmin):
    model = ProgramType
    menu_label = 'Program Type'
    menu_icon = 'tag'
    list_display = ('name', 'slug')
    list_display_add_buttons = 'slug'


class ProgramDeliveryAdmin(ModelAdmin):
    model = ProgramDelivery
    menu_label = 'Program Delivery'
    menu_icon = 'tag'
    list_display = ('name', 'slug')
    list_display_add_buttons = 'slug'


class ProgramLocationAdmin(ModelAdmin):
    model = ProgramLocation
    menu_label = 'Program Location'
    menu_icon = 'tag'
    list_display = ('name', 'slug')
    list_display_add_buttons = 'slug'


class NYCNeighborhoodAdmin(ModelAdmin):
    model = NYCNeighborhood
    menu_label = 'NYC Neighborhood'
    menu_icon = 'tag'
    list_display = ('name', 'slug')
    list_display_add_buttons = 'slug'


class SessionStartAdmin(ModelAdmin):
    model = SessionStart
    menu_label = 'Session Start'
    menu_icon = 'tag'
    list_display = ('name', 'slug')
    list_display_add_buttons = 'slug'


class SessionLengthAdmin(ModelAdmin):
    model = SessionLength
    menu_label = 'Session Length'
    menu_icon = 'tag'
    list_display = ('name', 'slug')
    list_display_add_buttons = 'slug'


class FeesCategoryAdmin(ModelAdmin):
    model = FeesCategory
    menu_label = 'Fees Category'
    menu_icon = 'tag'
    list_display = ('name', 'slug')
    list_display_add_buttons = 'slug'


class GenderFilterAdmin(ModelAdmin):
    model = GenderFilter
    menu_label = 'Gender Filter'
    menu_icon = 'tag'
    list_display = ('name', 'slug')
    list_display_add_buttons = 'slug'


class FocusTopicAdmin(ModelAdmin):
    model = FocusTopic
    menu_label = 'Focus Topic'
    menu_icon = 'tag'
    list_display = ('name', 'slug')
    list_display_add_buttons = 'slug'


class AgeGroupAdmin(ModelAdmin):
    model = AgeGroup
    menu_label = 'Age Group'
    menu_icon = 'tag'
    list_display = ('name', 'slug')
    list_display_add_buttons = 'slug'


class ProgramAdmin(ModelAdmin):
    model = Program
    menu_label = 'Program'  # ditch this to use verbose_name_plural from model
    menu_icon = 'pilcrow'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('title', 'city', 'status_string', 'first_published_at', 'last_published_at',)
    list_filter = ('gotham_state',)
    search_fields = ('title')
    list_display_add_buttons = 'last_published_at'
    list_export = ('title', 'city', 'status_string', 'last_published_at')
    export_filename = 'programs_list_export'
    list_display_links = ('title',)
    
    def status_string(self, obj):
        return obj.status_string.title()
    
    status_string.short_description = 'Status'



class ResourceAcademicStageAdmin(ModelAdmin):
    model = ResourceAcademicStage
    menu_label = 'Academic Stage'
    menu_icon = 'folder-open-inverse'
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    list_display_add_buttons = 'slug'


class ResourceCategoryAdmin(ModelAdmin):
    model = ResourceCategory
    menu_label = 'Categories'
    menu_icon = 'tag'
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    list_display_add_buttons = 'slug'
    

class ResourceAdmin(ModelAdmin):
    model = Resource
    menu_label = 'Resource'
    menu_icon = 'doc-full-inverse'
    list_display = ('name', 'author', 'age_group',)
    list_display_links = None
    list_filter = ('categories', 'types', )
    search_fields = ('name',)
    list_display_add_buttons = 'age_group'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_export = ('name', 'author', 'age_group',)
    export_filename = 'resource_list_export'



class ProgramGroupAdmin(ModelAdminGroup):
    menu_label = 'Program Manager'
    menu_icon = 'folder'
    items = (
        ProgramAdmin,
        ProgramTypeAdmin,
        ProgramDeliveryAdmin,
        ProgramLocationAdmin,
        NYCNeighborhoodAdmin,
        SessionStartAdmin,
        SessionLengthAdmin,
        FeesCategoryAdmin,
        GenderFilterAdmin,
        FocusTopicAdmin,
        AgeGroupAdmin,
    )


class ResourceGroupAdmin(ModelAdminGroup):
    menu_label = 'Resource Manager'
    menu_icon = 'folder'
    items = (
        ResourceAdmin, 
        ResourceAcademicStageAdmin, 
        ResourceCategoryAdmin
    )


modeladmin_register(ProgramGroupAdmin)
modeladmin_register(ResourceGroupAdmin)
