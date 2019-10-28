import sys
from concurrent.futures import ThreadPoolExecutor
from django.core.management.base import BaseCommand
from requests_html import HTMLSession
from fashion_catalogue.models import *
from datetime import datetime
from slugify import slugify
from queue import Queue
import os
import random
from threading import Lock
import logging

LOCKER = Lock()
logger = logging.getLogger('django')

with open(os.path.join('fashion_catalogue/management/commands/new_users.txt'), 'r', encoding='utf-8') as f:
    user_agents = f.read().split('\n')

with open(os.path.join('fashion_catalogue/management/commands/fresh_socks.txt'), 'r', encoding='utf-8') as f:
    proxies_list = f.read().split('\n')


def crawler(qu, task):
    while True:
        url = qu.get()

        with HTMLSession() as session:
            try:
                prox = random.choice(proxies_list)
                proxies = {'http': prox, 'https': prox}
                headers = {'User-Agent': str(random.choice(user_agents)).strip("\t\t\t\t")}
                response = session.get(url, proxies=proxies, headers=headers, timeout=10)
                name = response.html.xpath('//h1[@itemprop="name"]/text()')
                description = response.html.xpath('//div[@class="full-text"]/*')
                description = [elem.text for elem in description]
                description = ''.join([f'<p>{p}</p>' for p in description[0].split("\n") if p])
                slug = slugify(name[0])
                image_url = response.html.xpath('//img[@itemprop="image"]/@src')[0]
                try:
                    with HTMLSession() as session2:
                        resp_img = session2.get(image_url)
                        image_name = 'images/' + slug + '.' + image_url.split(".")[-1]
                    with open(f'media/{image_name}', 'wb') as picture:
                        picture.write(resp_img.content)
                    del resp_img
                except Exception as e:
                    print(e, type(e), sys.exc_info()[-1].tb_lineno)
                    image_name = 'default.jpg'
                size = ['XS', 'S', 'M', 'L', 'XL']
                color = str(image_url).split("/")[-2]
                category = str(url).split("/")[-3].split("-")[-1]

                price = response.html.xpath('//div[@class="price-info js-price-section"]/span/text()')
                price = float(str(price[1]).replace("$", '').replace("\n", '').replace("\t", ''))

                fashion = {
                    'name': name[0],
                    'slug': slug,
                    'description': description,
                    'img': image_name,
                    'image_url': image_url,
                    'price': price,
                    'item_source': url,
                    'parsing_date': datetime.now().date(),
                }
                with LOCKER:
                    if task:
                        task.status = f"Parsing: {url}"
                        task.save()
                    try:
                        item = FashionItem.objects.create(**fashion)
                        print('[Item saved]', fashion["name"], fashion["price"])
                    except Exception as e:
                        print('Не удалось записать позицию', type(e), e)
                        return
                    for s in size:
                        s, created = Size.objects.get_or_create(name=s)
                        item.size.add(s)
                    color, created = Color.objects.get_or_create(name=color)
                    item.color.add(color)
                    category = {'name': category, 'slug': slugify(category)}
                    category, created = Category.objects.get_or_create(**category)
                    item.cat.add(category)
                    logger.debug(item)

            except Exception as e:
                print(e, type(e))
                qu.put(url)
        if qu.empty():
            break


def run_parser(start, end, task):
    if task:
        if end <= start:
            task.status = 'Wrong input! End point lower or equal than start'
            task.save()
            return
        else:
            task.status = 'start parsing'
            task.save()

    with HTMLSession() as primary_session:
        try:
            prime_response = primary_session.get("https://www.ezibuy.com/shop/au/sitemap/WomensWearProduct-AU.xml")
            urls = prime_response.html.xpath("//url/loc/text()")
            # adding sitemap file for backup just in case
            with open(f'fashion_catalogue/management/commands/sitemap.txt', 'w') as sitemap:
                sitemap.write('\n'.join(urls))
        except Exception as e:
            print(e, type(e))

    urls_queue = Queue()

    with open(os.path.join('fashion_catalogue/management/commands/sitemap.txt'), 'r', encoding='utf-8') as file:
        count = len(open(os.path.join('fashion_catalogue/management/commands/sitemap.txt')).readlines())
        start = start if start <= count else 0
        end = end if end <= count else count
        try:
            urls = file.readlines()[start:end]
        except Exception as e:
            print(e, type(e))
        for url in urls:
            url = url.strip("\n")
            urls_queue.put(url)

    workers_count = 30 if (end - start) > 30 else abs(end - start)

    with ThreadPoolExecutor(max_workers=workers_count) as executor:
        for _ in range(workers_count):
            executor.submit(crawler, urls_queue, task)
    task.status = 'PARSING DONE!'
    task.end_time = datetime.now()
    task.save()


class Command(BaseCommand):
    help = 'Running fashion_items parser to database'

    def handle(self, *args, **options):
        from task.models import Task
        task = Task.objects.create(name='run_parser')
        run_parser(0, 10, task)
        print('Done')
