from wagtail import hooks
from django.utils.html import format_html

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
