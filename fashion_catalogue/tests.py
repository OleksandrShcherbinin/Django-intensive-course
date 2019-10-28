from django.test import TestCase, RequestFactory, Client
from .management.commands.get_fashion import crawler
from .models import *
from queue import Queue
from .views import IndexView


class FashionItemTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_crawler(self):
        count = FashionItem.objects.all().count()
        self.assertEqual(count, 0)
        url = "https://www.ezibuy.com/shop/au/sara-floral-lace-jacket/p/233845"
        qu = Queue()
        qu.put(url)
        crawler(qu, None)
        count = FashionItem.objects.all().count()
        self.assertEqual(count, 1)

    def test_fashion_structure(self):
        price = hasattr(FashionItem, 'price')
        self.assertTrue(price)

    def test_reviews_model(self):
        rating = hasattr(Reviews, 'rating')
        self.assertTrue(rating)

    def test_category_models(self):
        slug = hasattr(Category, 'slug')
        self.assertTrue(slug)

    def test_index_view(self):
        request = self.factory.get('/')
        index_object = IndexView()
        index_object.request = request
        result = index_object.get_context_data()
        self.assertTrue('fashion' and 'banners' in result)

    def test_client(self):
        c = Client()
        response = c.post('/login/',
                          {'username': 'Oleksandr_Shcherbinin',
                           'password': 'kv;lvlhlvkshvl'})
        status = response.status_code
        response = c.get('/')
        type_content = response.content
        self.assertTrue(status, 200 and type_content is "b'<!DOCTYPE html...")


class FashionItemModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Color.objects.create(name='Blue')
        Category.objects.create(name='Jeans',
                                slug='jeans',)
        Size.objects.create(name='M')
        cat = Category.objects.filter(pk=1)
        color = Color.objects.get(pk=1)
        size = Size.objects.get(pk=1)

        fashion_item = FashionItem(name='Skinny Blue Jeans',
                                   slug='skinny-blue-jeans',
                                   description='Very beautiful jeans for ladies!',
                                   img='https://media.ezibuy.com/productimages/244011/White/'
                                       'Next_Stripe_Cold_Shoulder_Linen_Jumpsuit_Detail_1_10150649954334.jpg',
                                   price=100,

                                   parsing_date='2019-10-17 18:00'
                                   )
        fashion_item.save()
        fashion_item.cat.set(cat)
        fashion_item.size.add(size)
        fashion_item.color.add(color)

    def test_name_label(self):
        fashion_item = FashionItem.objects.get(id=1)
        field_label = fashion_item._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_slug_label(self):
        fashion_item = FashionItem.objects.get(id=1)
        field_label = fashion_item._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'slug')

    def test_description_label(self):
        fashion_item = FashionItem.objects.get(id=1)
        field_label = fashion_item._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_category_label(self):
        fashion_item = FashionItem.objects.get(id=1)
        field_label = fashion_item._meta.get_field('cat').verbose_name
        self.assertEquals(field_label, 'cat')

    def test_parsing_date_label(self):
        fashion_item = FashionItem.objects.get(id=1)
        field_label = fashion_item._meta.get_field('parsing_date').verbose_name
        self.assertEquals(field_label, 'parsing date')

    def test_color_label(self):
        fashion_item = FashionItem.objects.get(id=1)
        field_label = fashion_item._meta.get_field('color').verbose_name
        self.assertEquals(field_label, 'color')

    def test_image_label(self):
        fashion_item = FashionItem.objects.get(id=1)
        field_label = fashion_item._meta.get_field('img').verbose_name
        self.assertEquals(field_label, 'img')

    def test_name_value(self):
        fashion_item = FashionItem.objects.get(id=1)
        field_value = fashion_item.name
        self.assertEquals(field_value, 'Skinny Blue Jeans')

    def test_slug_value(self):
        fashion_item = FashionItem.objects.get(id=1)
        field_value = fashion_item.slug
        self.assertEquals(field_value, 'skinny-blue-jeans')

    def test_description_value(self):
        fashion_item = FashionItem.objects.get(id=1)
        field_value = fashion_item.description
        self.assertEquals(field_value, 'Very beautiful jeans for ladies!')

    def test_category_value(self):
        fashion_item = FashionItem.objects.get(id=1)
        field_value = fashion_item.cat.all()[0]
        self.assertEquals(field_value.name, 'Jeans')

    def test_parsing_date_value(self):
        fashion_item = FashionItem.objects.get(id=1)
        field_value = str(fashion_item.parsing_date)
        self.assertEquals(field_value, '2019-10-17 15:00:00+00:00')

    def test_color_value(self):
        fashion_item = FashionItem.objects.get(id=1)
        field_value = fashion_item.color.all()[0]
        self.assertEquals(field_value.name, 'Blue')

    def test_size_value(self):
        fashion_item = FashionItem.objects.get(id=1)
        field_value = fashion_item.size.all()[0]
        self.assertEquals(field_value.name, 'M')

    def test_image_value(self):
        fashion_item = FashionItem.objects.get(id=1)
        field_value = fashion_item.img
        self.assertEquals(field_value, 'https://media.ezibuy.com/productimages/244011/White/'
                                       'Next_Stripe_Cold_Shoulder_Linen_Jumpsuit_Detail_1_10150649954334.jpg')

    def test_category_type(self):
        fashion_item = FashionItem.objects.get(id=1)
        for category in fashion_item.cat.all():
            field_value = category
            self.assertEquals(type(field_value), Category)

    def test_color_type(self):
        fashion_item = FashionItem.objects.get(id=1)
        for color in fashion_item.color.all():
            field_value = color
            self.assertEquals(type(field_value), Color)

    def test_object_name_in_the_str_format(self):
        fashion_item = FashionItem.objects.get(id=1)
        expected_object_name = 'Skinny Blue Jeans'
        self.assertEquals(expected_object_name, str(fashion_item))

    def test_slug_max_length(self):
        fashion_item = FashionItem.objects.get(id=1)
        max_length = fashion_item._meta.get_field('slug').max_length
        self.assertEquals(max_length, 255)


class CheckResponseTest(TestCase):

    def setUp(self):
        Color.objects.create(name='Blue')
        Category.objects.create(name='Jeans',
                                slug='jeans', )
        Size.objects.create(name='M')
        cat = Category.objects.filter(pk=1)
        color = Color.objects.get(pk=1)
        size = Size.objects.get(pk=1)

        fashion_item = FashionItem(name='Skinny Blue Jeans',
                                   slug='skinny-blue-jeans',
                                   description='Very beautiful jeans for ladies!',
                                   img='https://media.ezibuy.com/productimages/244011/White/'
                                       'Next_Stripe_Cold_Shoulder_Linen_Jumpsuit_Detail_1_10150649954334.jpg',
                                   price=100,

                                   parsing_date='2019-10-17 18:00'
                                   )
        fashion_item.save()
        fashion_item.cat.set(cat)
        fashion_item.size.add(size)
        fashion_item.color.add(color)

        self.cat = cat[0]
        self.color = color
        self.size = size
        self.fashion_item = fashion_item
        self.client = Client()

    def test_index(self):
        url = ''
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_fashion_items_detail(self):
        response = self.client.get(f'product/{self.fashion_item.slug}')
        self.assertEqual(response.status_code, 200)

    def test_categories(self):
        response = self.client.get(self.cat.slug)
        self.assertEqual(response.status_code, 200)

    def test_colors(self):
        response = self.client.get(self.color.name)
        self.assertEqual(response.status_code, 200)

