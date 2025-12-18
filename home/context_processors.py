from django.core.cache import cache
from wagtail.models import Site, Page


def site_info(request):
    site = Site.find_for_request(request)
    if site and site.root_page:
        root_page = site.root_page
        top_level_pages = root_page.get_children().live().in_menu()
        cache_key = f"site_pages_{root_page.id}"

        data = None#cache.get(cache_key)
        top_level_pages = root_page.get_children().live().in_menu()
        
        if not data:
            pages = {page.slug: page for page in top_level_pages}
            data = {"site_pages": pages}
            cache.set(cache_key, data, 300)  # 5 minutes

        return data

    return {}