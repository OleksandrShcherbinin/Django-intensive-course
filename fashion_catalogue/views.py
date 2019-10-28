from django.shortcuts import render
from .models import FashionItem, Size, Color, Category, Reviews
import random
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic import FormView
from django.views.generic.list import ListView
from django.http import Http404
from django.contrib import messages
from .forms import ReviewForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
import logging

logger = logging.getLogger('django')


class IndexView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixed = random.randrange(0, 1000)
        fashion = FashionItem.objects.all()[mixed:mixed + 8]
        context.update({'fashion': fashion})
        banner_numbers = random.sample(range(1, 15), 3)
        banners = []
        for banner in banner_numbers:
            banners.append(f"images/banner/banner-{banner}.jpg")
        context.update({'banners': banners})
        logger.debug(context)
        return context


@method_decorator(csrf_protect, name='dispatch')
class ProductView(DetailView, FormView, SingleObjectMixin):
    template_name = 'product.html'
    model = FashionItem
    context_object_name = 'product'
    slug_url_kwarg = 'slug'
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        mixed_pics = random.randrange(0, 1500)
        context = super().get_context_data(**kwargs)
        pics = FashionItem.objects.all()[mixed_pics:mixed_pics + 3]
        sizes = Size.objects.all()
        color = Color.objects.get(fashionitem=self.object)
        context.update({'sizes': sizes})
        context.update({'pics': pics})
        context.update({'color': color})

        context['reviews'] = Reviews.objects.filter(fashion_item=self.object,
                                                    moderated=True).order_by('-published')[:5]
        return context

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        self.form = ReviewForm(self.request.POST)
        context = self.get_context_data(**kwargs)
        if self.form.is_valid():
            Reviews.objects.create(**self.form.cleaned_data, fashion_item=self.object)
            messages.add_message(self.request, messages.INFO, 'Thank you! Your review is on moderation!')
        else:
            logger.warning(self.form)
            context['form'] = self.form
            messages.add_message(self.request, messages.INFO, 'Incorrect input! Try one more time!')
        return self.render_to_response(context)


class CatalogueView(ListView, SingleObjectMixin):
    template_name = 'catalogue.html'
    model = FashionItem
    paginate_by = 12
    slug_field = 'slug'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Category.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        color = self.request.GET.get('color')
        if color:
            return FashionItem.objects.filter(cat=self.object, color__name=color)
        return FashionItem.objects.filter(cat=self.object)

    def get_context_data(self, *, object_list=None, **kwargs):
        mixed = random.randrange(0, 1000)
        cat_mix = random.randrange(0, 100)
        context = super().get_context_data(**kwargs)
        categ_products = FashionItem.objects.filter(cat=self.object.id)
        colores = Color.objects.filter(name=self.object)
        pop_fashion = FashionItem.objects.all()[mixed:mixed + 3]
        cat_small = Category.objects.all()[cat_mix: cat_mix + 10]
        context['categ_products'] = categ_products
        context['pop_fashion'] = pop_fashion
        context['cat_small'] = cat_small
        context['color'] = colores

        return context


class SearchView(ListView):
    template_name = 'catalogue.html'
    model = FashionItem
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q')
        color = self.request.GET.get('color')
        if query:
            return FashionItem.objects.filter(name__contains=query)
        elif color:
            return FashionItem.objects.filter(color__name=color)[:9]
        else:
            return Http404()


def robots_view(request):
    return render(request, 'robots.txt', {}, content_type="text/plain")