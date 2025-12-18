from django.shortcuts import render
# Import Paginator for pagination logic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from wagtail.models import Page
from django.db.models import Q
import logging

# Set up logging
logger = logging.getLogger(__name__)
