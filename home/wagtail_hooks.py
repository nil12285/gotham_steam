from django.urls import path
from django.http import HttpResponse
from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks
from wagtail.admin.rich_text.editors.draftail import features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineStyleElementHandler,
    InlineEntityElementHandler
) 
from wagtail.admin.modal_workflow import render_modal_workflow

# @hooks.register('insert_global_admin_css')
# def global_admin_css():
#     return format_html(
#         '<link rel="stylesheet" href="{}">', 
#         static('css/bootstrap.min.css')
#     )


# @hooks.register("insert_global_admin_js")
# def add_admin_bootstrap_js():
#     return format_html(
#         '<script src="{}"></script>', 
#         static('js/admin_bootstrap.js')
#     )

