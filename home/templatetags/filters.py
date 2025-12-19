from django.conf import settings
import json
from collections import OrderedDict
import re
from datetime import datetime, timedelta
from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from logging import getLogger
from django.utils.encoding import iri_to_uri
from django.template.loader import get_template

logger = getLogger("root")

localization = True
if hasattr(settings, 'USE_I18N'):
    localization = settings.USE_I18N

register= template.Library()

@register.filter(name= 'name_apostrophe')
def exists(value):
    if value[-1:].lower()=='s':
        return value + '\''
    else:
        return value + '\'s'
    

@register.filter
def obj_type(obj):
    return type(obj).__name__

    
@register.filter
def lookup(obj, key):
    if not obj or not key:
        return ''
    val = ''
    
    if type(obj) in (dict, OrderedDict):
        val = obj.get(key,'')
    else:
        if hasattr(obj, key):
            val =  getattr(obj, str(key))
        elif len(key.split('.'))>1:
            stmnt = 'val = obj.{}'.format(key)
            _locals = locals()
            try:
                exec(stmnt, globals(), _locals)
            except Exception as e:
                pass

            val = _locals['val']
                
    if val is None:
        return '' 
    return val


@register.filter
def slugify(value):
    if value:
        return value.replace(" ","-")


@register.filter
def dict__(value):
    try:
        return f"{value.__dict__}"
    except:
        return None
    
@register.filter
def jsonify(value):
    # If we have a queryset, then convert it into a list.
    if getattr(value, 'all', False):
        value = list(value)
    return mark_safe(json.dumps(value))



@register.filter
def date_to_str(value, format):
    try:
        return value.strftime(format)
    except Exception as e:
        logger.error(e)
        return ''

@register.filter
def to_date(value, dformat='%Y-%m-%d'):
    if value:
        return datetime.strptime(value, dformat)


@register.filter()
def add_days(days):
    return now() + timedelta(days=days)


@register.filter()
def number_format(number):
    if number:
        return number
    else:
        return '-'


@register.filter
def split(string, split_with=" "):
    if string:
        return string.split(split_with)
    

@register.simple_tag
def selected_filter(cl, spec):
    selected_filter_html = ""
    for choice in list(spec.choices(cl)):
        if choice.get('selected'):
            qstring = ''.join([f'{k}={v}' for k,v in spec.used_parameters.items()])
            tpl = get_template('admin/includes/selected_filter.html')
            selected_filter_html += "\n" + tpl.render({
                'un_select_url' : iri_to_uri(choice['query_string']).replace(iri_to_uri(qstring),''),
                'title' : spec.title,
                'selected_value' : choice['display'],
            })
        else:
            if choice.get('form'):
                tpl = get_template('admin/includes/selected_filter.html')
                query_string = f"?{spec.request.META['QUERY_STRING']}"
                for k,v in spec.used_parameters.items():
                    query_string = query_string.replace(f'{k}={v}','')
                if query_string:
                    while query_string[-1] == '&':
                        query_string = query_string[:-1]
                from_param = f'{spec.field_path}_from'
                to_param = f'{spec.field_path}_to'
                selected_filter_html += "\n" + tpl.render({
                    'un_select_url' : iri_to_uri(query_string),
                    'title' : spec.title,
                    'selected_value' : f"{spec.used_parameters[from_param]} - {spec.used_parameters[to_param] if spec.used_parameters[to_param] else '∞'}",
                })

    return mark_safe(selected_filter_html)
                

@register.filter
def replace(value, arg):
    """
    Replacing filter
    Use `{{ "aaa"|replace:"a|b" }}`
    """
    if len(arg.split('|')) != 2:
        return value

    what, to = arg.split('|')
    return value.replace(what, to)
