from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
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
    AgeGroup
)

class ProgramTypeAdmin(ModelAdmin):
    model = ProgramType
    menu_label = 'Program Type'
    menu_icon = 'tag'
    list_display = ('name', 'slug')


class ProgramDeliveryAdmin(ModelAdmin):
    model = ProgramDelivery
    menu_label = 'Program Delivery'
    menu_icon = 'tag'
    list_display = ('name', 'slug')


class ProgramLocationAdmin(ModelAdmin):
    model = ProgramLocation
    menu_label = 'Program Location'
    menu_icon = 'tag'
    list_display = ('name', 'slug')


class NYCNeighborhoodAdmin(ModelAdmin):
    model = NYCNeighborhood
    menu_label = 'NYC Neighborhood'
    menu_icon = 'tag'
    list_display = ('name', 'slug')


class SessionStartAdmin(ModelAdmin):
    model = SessionStart
    menu_label = 'Session Start'
    menu_icon = 'tag'
    list_display = ('name', 'slug')


class SessionLengthAdmin(ModelAdmin):
    model = SessionLength
    menu_label = 'Session Length'
    menu_icon = 'tag'
    list_display = ('name', 'slug')


class FeesCategoryAdmin(ModelAdmin):
    model = FeesCategory
    menu_label = 'Fees Category'
    menu_icon = 'tag'
    list_display = ('name', 'slug')


class GenderFilterAdmin(ModelAdmin):
    model = GenderFilter
    menu_label = 'Gender Filter'
    menu_icon = 'tag'
    list_display = ('name', 'slug')


class FocusTopicAdmin(ModelAdmin):
    model = FocusTopic
    menu_label = 'Focus Topic'
    menu_icon = 'tag'
    list_display = ('name', 'slug')


class AgeGroupAdmin(ModelAdmin):
    model = AgeGroup
    menu_label = 'Age Group'
    menu_icon = 'tag'
    list_display = ('name', 'slug')



class ProgramAdmin(ModelAdmin):
    model = Program
    menu_label = 'Program'  # ditch this to use verbose_name_plural from model
    menu_icon = 'pilcrow'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('title', 'city', 'status_string', 'first_published_at', 'last_published_at', 'action_buttons')
    list_filter = ('gotham_state',)
    search_fields = ('title')
    list_display_add_buttons = 'action_buttons'
    list_export = ('title', 'city', 'status_string', 'last_published_at')
    export_filename = 'programs_list_export'
    
    def action_buttons(self, obj):
        return '' 
    
    def status_string(self, obj):
        return obj.status_string.title()
    
    action_buttons.short_description = 'Actions'
    status_string.short_description = 'Status'

modeladmin_register(ProgramAdmin)
modeladmin_register(ProgramTypeAdmin)
modeladmin_register(ProgramDeliveryAdmin)
modeladmin_register(ProgramLocationAdmin)
modeladmin_register(NYCNeighborhoodAdmin)
modeladmin_register(SessionStartAdmin)
modeladmin_register(SessionLengthAdmin)
modeladmin_register(FeesCategoryAdmin)
modeladmin_register(GenderFilterAdmin)
modeladmin_register(FocusTopicAdmin)
modeladmin_register(AgeGroupAdmin)