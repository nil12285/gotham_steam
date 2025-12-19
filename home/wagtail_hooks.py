from django.utils.html import format_html
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from .models import Program


# @hooks.register("insert_global_admin_css")
# def add_bootstrap_css():
#     return format_html(
#         '<link rel="stylesheet" '
#         'href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">'
#     )

# @hooks.register("insert_global_admin_js")
# def add_bootstrap_js():
#     return format_html(
#         """
#         <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
#         <script src="/static/js/admin_bootstrap.js"></script>
#         """
#     )




class ProgramAdmin(ModelAdmin):
    model = Program
    menu_label = 'Program'  # ditch this to use verbose_name_plural from model
    menu_icon = 'pilcrow'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('title', 'city', 'status_string', 'first_published_at', 'last_published_at', 'action_buttons')
    list_filter = ('city',)
    search_fields = ('title')
    list_display_add_buttons = 'action_buttons'
    list_export = ('title', 'city', 'status_string', 'first_published_at', 'last_published_at')
    export_filename = 'programs_list_export'
    
    def action_buttons(self, obj):
        return '' 
    
    def status_string(self, obj):
        return obj.status_string.title()
    
    action_buttons.short_description = 'Actions'
    status_string.short_description = 'Status'

modeladmin_register(ProgramAdmin)
