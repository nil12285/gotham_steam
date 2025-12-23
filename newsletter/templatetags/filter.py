from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from django import template
from django.conf import settings

register = template.Library()

@register.filter
def add_utm(url, params=None):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    defaults = settings.NEWSLETTER_UTM_DEFAULTS.copy()
    if params:
        defaults.update(params)

    for k, v in defaults.items():
        query[k] = v

    new_query = urlencode(query, doseq=True)
    return urlunparse(parsed._replace(query=new_query))


