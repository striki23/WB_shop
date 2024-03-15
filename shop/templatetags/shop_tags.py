from django import template
from datetime import datetime
import shop.models as models

register = template.Library()


@register.simple_tag()
def get_categories():
    categories = models.Category.objects.all()
    return categories


@register.simple_tag()
def get_year():
    current_year = datetime.now().year
    return current_year
