from django.db.models.signals import post_save
from fashion_catalogue.models import FashionItem, Category
from .models import Task
from fashion_catalogue.management.commands.get_fashion import run_parser
from threading import Thread
import os
from django.conf import settings


def handler_run_parser(sender, instance, **kwargs):
    if kwargs.get('created'):
        if instance.task == 'run_parser':
            try:
                start, end = instance.arg.split(',')
                start, end = int(start), int(end)
            except Exception as e:
                print(e, type(e))
                start, end = 0, 1
            Thread(target=run_parser, args=(start, end, instance)).start()
        elif instance.task == 'count_images':
            count_images = len(os.listdir(os.path.join(settings.BASE_DIR, 'media/images/')))
            instance.status = f'Images = {count_images}'
            instance.save()
        elif instance.task == 'show__items_number':
            count_items = FashionItem.objects.count()
            instance.status = f'There are {count_items} items in your fashion catalogue'
            instance.save()
        elif instance.task == 'show_categories_number':
            count_categories = Category.objects.count()
            instance.status = f'There are {count_categories} categories in your database'
            instance.save()


post_save.connect(handler_run_parser, sender=Task)
