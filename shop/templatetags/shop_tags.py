from django import template
import shop.models as models

register = template.Library()


@register.simple_tag()
def get_categories():
    categories = models.Category.objects.all()
    return categories
