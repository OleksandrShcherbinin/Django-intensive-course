from .models import Category, Color, Size
from django.db.models import Count
from cache_memoize import cache_memoize


@cache_memoize(3600)
def menu(request):
    categs = Category.objects.annotate(fashion_count=Count('fashionitem')).order_by('-fashion_count')[:20]
    colors = Color.objects.annotate(color_count=Count('fashionitem')).order_by('-color_count')[:20]
    return {'categories': categs, 'colors': colors, }
