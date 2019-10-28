from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from fashion_catalogue.models import Category, FashionItem, Color, Size, Reviews


class FashionItemAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_filter = ['color']
    list_display = ['name', 'item_source', 'parsing_date', 'price']
    list_editable = ['price']
    search_fields = ['description']


class ReviewAdmin(SummernoteModelAdmin):
    summernote_fields = ('comment',)
    list_filter = ['published', 'moderated', 'rating']
    list_display = ['name', 'email', 'published', 'moderated']
    list_editable = ['moderated']
    search_fields = ['name', 'description']


admin.site.register(Category)
admin.site.register(FashionItem, FashionItemAdmin)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Reviews, ReviewAdmin)

